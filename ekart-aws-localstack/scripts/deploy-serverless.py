#!/usr/bin/env python3
"""
Complete Serverless Deployment Script for EKart Store on LocalStack
Deploys: DynamoDB, Cognito, S3, Lambda Functions, API Gateway
"""
import boto3
import json
import time
import zipfile
import os
import subprocess
from pathlib import Path

# LocalStack configuration (read from serverless-config.json)
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'serverless-config.json'
with open(CONFIG_PATH, 'r') as _cfg_file:
    _CFG = json.load(_cfg_file)

ENDPOINT = _CFG.get('endpoint')
REGION = _CFG.get('region')
ENV = _CFG.get('env', 'dev')
LAMBDA_ENDPOINT = _CFG.get('lambda_endpoint', 'http://localhost.localstack.cloud:4566')

def create_aws_clients():
    """Create AWS clients for LocalStack"""
    config = {
        'endpoint_url': ENDPOINT,
        'region_name': REGION,
        'aws_access_key_id': 'test',
        'aws_secret_access_key': 'test'
    }
    
    return {
        'dynamodb': boto3.client('dynamodb', **config),
        'cognito': boto3.client('cognito-idp', **config),
        's3': boto3.client('s3', **config),
        'lambda_client': boto3.client('lambda', **config),
        'apigateway': boto3.client('apigateway', **config),
        'iam': boto3.client('iam', **config)
    }

def create_dynamodb_tables(dynamodb):
    """Create DynamoDB tables"""
    print("📦 Creating DynamoDB tables...")
    
    tables = [
        {
            'TableName': f'ekart-users-{ENV}',
            'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [{
                'IndexName': 'email-index',
                'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-products-{ENV}',
            'KeySchema': [{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [
                {'AttributeName': 'product_id', 'AttributeType': 'S'},
                {'AttributeName': 'seller_id', 'AttributeType': 'S'},
                {'AttributeName': 'category', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'seller-index',
                    'KeySchema': [{'AttributeName': 'seller_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'category-index',
                    'KeySchema': [{'AttributeName': 'category', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-orders-{ENV}',
            'KeySchema': [{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'buyer_id', 'AttributeType': 'S'},
                {'AttributeName': 'seller_id', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'buyer-index',
                    'KeySchema': [{'AttributeName': 'buyer_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'seller-index',
                    'KeySchema': [{'AttributeName': 'seller_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-carts-{ENV}',
            'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [{'AttributeName': 'user_id', 'AttributeType': 'S'}],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': f'ekart-inventory-{ENV}',
            'KeySchema': [{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            'AttributeDefinitions': [{'AttributeName': 'product_id', 'AttributeType': 'S'}],
            'BillingMode': 'PAY_PER_REQUEST'
        }
    ]
    
    for table_config in tables:
        try:
            dynamodb.create_table(**table_config)
            print(f"  ✓ Created table: {table_config['TableName']}")
        except dynamodb.exceptions.ResourceInUseException:
            print(f"  ⚠ Table already exists: {table_config['TableName']}")
        except Exception as e:
            print(f"  ✗ Error creating table {table_config['TableName']}: {e}")

def create_cognito_user_pool(cognito):
    """Create Cognito user pool with custom attributes"""
    print("🔐 Creating Cognito user pool...")
    
    try:
        # Create user pool with custom attributes
        response = cognito.create_user_pool(
            PoolName=f'ekart-users-{ENV}',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': False,
                    'RequireLowercase': False,
                    'RequireNumbers': False,
                    'RequireSymbols': False
                }
            },
            AutoVerifiedAttributes=['email'],
            Schema=[
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'Required': True,
                    'Mutable': True
                },
                {
                    'Name': 'custom:user_type',
                    'AttributeDataType': 'String',
                    'Mutable': True
                },
                {
                    'Name': 'custom:first_name',
                    'AttributeDataType': 'String',
                    'Mutable': True
                },
                {
                    'Name': 'custom:last_name',
                    'AttributeDataType': 'String',
                    'Mutable': True
                }
            ]
        )
        user_pool_id = response['UserPool']['Id']
        print(f"  ✓ Created user pool: {user_pool_id}")
        
        # Create user pool client with USER_PASSWORD_AUTH
        client_response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=f'ekart-client-{ENV}',
            ExplicitAuthFlows=[
                'ALLOW_USER_PASSWORD_AUTH',
                'ALLOW_USER_SRP_AUTH',
                'ALLOW_REFRESH_TOKEN_AUTH'
            ],
            GenerateSecret=False,
            PreventUserExistenceErrors='ENABLED'
        )
        client_id = client_response['UserPoolClient']['ClientId']
        print(f"  ✓ Created user pool client: {client_id}")
        
        return user_pool_id, client_id
        
    except cognito.exceptions.ResourceConflictException:
        print(f"  ⚠ User pool already exists")
        # List existing pools to get ID
        pools = cognito.list_user_pools(MaxResults=10)
        for pool in pools.get('UserPools', []):
            if pool['Name'] == f'ekart-users-{ENV}':
                user_pool_id = pool['Id']
                # Get client ID
                clients = cognito.list_user_pool_clients(UserPoolId=user_pool_id, MaxResults=10)
                client_id = clients['UserPoolClients'][0]['ClientId'] if clients.get('UserPoolClients') else None
                return user_pool_id, client_id
    except Exception as e:
        print(f"  ✗ Error creating user pool: {e}")
        return None, None

def create_s3_buckets(s3):
    """Create S3 buckets"""
    print("🪣 Creating S3 buckets...")
    
    buckets = [f'ekart-product-images-{ENV}', f'ekart-lambda-code-{ENV}']
    
    for bucket_name in buckets:
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"  ✓ Created bucket: {bucket_name}")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            print(f"  ⚠ Bucket already exists: {bucket_name}")
        except Exception as e:
            print(f"  ✗ Error creating bucket {bucket_name}: {e}")

def create_lambda_role(iam):
    """Create IAM role for Lambda functions"""
    print("👤 Creating Lambda execution role...")
    
    role_name = f'ekart-lambda-role-{ENV}'
    
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description='Lambda execution role for EKart'
        )
        role_arn = response['Role']['Arn']
        print(f"  ✓ Created role: {role_name}")
        
        # Attach policies (LocalStack doesn't enforce permissions, but we create them for completeness)
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
        return role_arn
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"  ⚠ Role already exists: {role_name}")
        response = iam.get_role(RoleName=role_name)
        return response['Role']['Arn']
    except Exception as e:
        print(f"  ✗ Error creating role: {e}")
        # For LocalStack, use a dummy ARN
        return f'arn:aws:iam::000000000000:role/{role_name}'

def create_lambda_deployment_package(function_dir):
    """Create ZIP deployment package for Lambda function"""
    zip_path = function_dir / 'function.zip'

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(function_dir):
            root_path = Path(root)
            # Skip existing zip files
            files_to_add = [f for f in files if f != 'function.zip']
            for file_name in files_to_add:
                full_path = root_path / file_name
                arcname = str(full_path.relative_to(function_dir))
                zipf.write(full_path, arcname)

    return zip_path

def deploy_lambda_functions(lambda_client, role_arn, user_pool_id, client_id):
    """Deploy all Lambda functions"""
    print("🚀 Deploying Lambda functions...")
    
    functions = [
        {
            'name': 'ekart-auth-api',
            'dir': 'auth-api',
            'handler': 'handler.lambda_handler',
            'env': {
                'USER_POOL_ID': user_pool_id,
                'CLIENT_ID': client_id,
                'USERS_TABLE': f'ekart-users-{ENV}',
                'AWS_ENDPOINT_URL': LAMBDA_ENDPOINT
            }
        },
        {
            'name': 'ekart-products-api',
            'dir': 'products-api',
            'handler': 'handler.lambda_handler',
            'env': {
                'PRODUCTS_TABLE': f'ekart-products-{ENV}',
                'AWS_ENDPOINT_URL': LAMBDA_ENDPOINT
            }
        },
        {
            'name': 'ekart-cart-api',
            'dir': 'cart-api',
            'handler': 'handler.lambda_handler',
            'env': {
                'CARTS_TABLE': f'ekart-carts-{ENV}',
                'PRODUCTS_TABLE': f'ekart-products-{ENV}',
                'AWS_ENDPOINT_URL': LAMBDA_ENDPOINT
            }
        },
        {
            'name': 'ekart-orders-api',
            'dir': 'orders-api',
            'handler': 'handler.lambda_handler',
            'env': {
                'ORDERS_TABLE': f'ekart-orders-{ENV}',
                'CARTS_TABLE': f'ekart-carts-{ENV}',
                'PRODUCTS_TABLE': f'ekart-products-{ENV}',
                'AWS_ENDPOINT_URL': LAMBDA_ENDPOINT
            }
        },
        {
            'name': 'ekart-payment-processor',
            'dir': 'payment-processor',
            'handler': 'handler.lambda_handler',
            'env': {
                'AWS_ENDPOINT_URL': LAMBDA_ENDPOINT,
                'STRIPE_BASE_URL': f"{LAMBDA_ENDPOINT}/stripe",
                'STRIPE_API_KEY': 'sk_test_12345'
            }
        }
    ]
    
    deployed_functions = {}
    
    for func in functions:
        try:
            function_dir = PROJECT_ROOT / 'lambda-functions' / func['dir']
            # Install requirements.txt if present
            requirements_path = function_dir / 'requirements.txt'
            if requirements_path.exists():
                    print(f"  📦 Installing dependencies for {func['dir']} with --upgrade...")
                    subprocess.run([
                        'pip', 'install', '-r', str(requirements_path), '-t', str(function_dir), '--upgrade'
                    ], check=True)
            zip_path = create_lambda_deployment_package(function_dir)
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            function_name = func['name']
            # Check if function exists
            try:
                lambda_client.get_function(FunctionName=function_name)
                print(f"  ⚠ Deleting existing function: {function_name}")
                lambda_client.delete_function(FunctionName=function_name)
                time.sleep(2)
            except lambda_client.exceptions.ResourceNotFoundException:
                pass
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role=role_arn,
                Handler=func['handler'],
                Code={'ZipFile': zip_content},
                Environment={'Variables': func['env']},
                Timeout=30,
                MemorySize=256
            )
            print(f"  ✓ Created function: {function_name}")
            response = lambda_client.get_function(FunctionName=function_name)
            deployed_functions[func['dir']] = response['Configuration']['FunctionArn']
            # Clean up zip file
            zip_path.unlink()
            
        except Exception as e:
            print(f"  ✗ Error deploying {func['name']}: {e}")
    
    return deployed_functions

def create_api_gateway(apigateway, lambda_client, lambda_functions, user_pool_id):
    """Create API Gateway with all routes"""
    print("🌐 Creating API Gateway...")
    
    try:
        # Create REST API
        api_name = f'ekart-api-{ENV}'
        
        # Try to find existing API and delete it (fresh start)
        apis = apigateway.get_rest_apis()
        for api in apis.get('items', []):
            if api['name'] == api_name:
                print(f"  ⚠ Deleting existing API: {api_name} ({api['id']})")
                try:
                    apigateway.delete_rest_api(restApiId=api['id'])
                    time.sleep(2)
                except:
                    pass
        
        # Create new API
        api_response = apigateway.create_rest_api(
            name=api_name,
            description='EKart Store API Gateway',
            endpointConfiguration={'types': ['REGIONAL']}
        )
        api_id = api_response['id']
        print(f"  ✓ Created API: {api_name} ({api_id})")
        
        # Get root resource
        resources = apigateway.get_resources(restApiId=api_id)
        root_id = resources['items'][0]['id']
        
        # Create /api resource
        api_resource_id = create_resource(apigateway, api_id, root_id, 'api')
        
        if not api_resource_id:
            print("  ✗ Failed to create /api resource")
            return None, None
        
        # Create routes
        routes = [
            {'path': 'auth', 'lambda_key': 'auth-api', 'methods': ['POST', 'GET']},
            {'path': 'products', 'lambda_key': 'products-api', 'methods': ['GET', 'POST', 'PUT', 'DELETE']},
            {'path': 'cart', 'lambda_key': 'cart-api', 'methods': ['GET', 'POST', 'PUT', 'DELETE']},
            {'path': 'orders', 'lambda_key': 'orders-api', 'methods': ['GET', 'POST', 'PUT']},
            {'path': 'payments', 'lambda_key': 'payment-processor', 'methods': ['POST']}
        ]
        
        for route in routes:
            if route['lambda_key'] in lambda_functions:
                resource_id = create_resource(apigateway, api_id, api_resource_id, route['path'])
                
                if not resource_id:
                    print(f"  ⚠ Skipping route: {route['path']}")
                    continue
                
                # Create {proxy+} resource for sub-paths
                proxy_resource_id = create_resource(apigateway, api_id, resource_id, '{proxy+}')
                
                # Create methods on proxy resource if it exists
                if proxy_resource_id:
                    for method in route['methods']:
                        create_method(
                            apigateway, lambda_client, api_id,
                            proxy_resource_id, method,
                            lambda_functions[route['lambda_key']]
                        )
                
                # Also create methods on parent resource
                for method in route['methods']:
                    create_method(
                        apigateway, lambda_client, api_id,
                        resource_id, method,
                        lambda_functions[route['lambda_key']]
                    )
        
        # Deploy API
        deployment = apigateway.create_deployment(
            restApiId=api_id,
            stageName=ENV
        )
        print(f"  ✓ Deployed API to stage: {ENV}")
        
        api_url = f"{ENDPOINT}/restapis/{api_id}/{ENV}/_user_request_"
        print(f"  ✓ API URL: {api_url}")
        
        return api_id, api_url
        
    except Exception as e:
        print(f"  ✗ Error creating API Gateway: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def create_resource(apigateway, api_id, parent_id, path_part):
    """Create API Gateway resource and return resource ID"""
    try:
        # Check if resource exists
        resources = apigateway.get_resources(restApiId=api_id)
        for resource in resources['items']:
            if resource.get('pathPart') == path_part and resource.get('parentId') == parent_id:
                return resource['id']
        
        # Create new resource
        response = apigateway.create_resource(
            restApiId=api_id,
            parentId=parent_id,
            pathPart=path_part
        )
        return response['id']
    except Exception as e:
        print(f"    Warning: Error creating resource {path_part}: {e}")
        return None

def create_method(apigateway, lambda_client, api_id, resource_id, http_method, lambda_arn):
    """Create API Gateway method and integration"""
    try:
        # Create method
        try:
            apigateway.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                authorizationType='NONE',
                apiKeyRequired=False
            )
        except apigateway.exceptions.ConflictException:
            pass  # Method already exists
        
        # Create integration
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
        )
        
        # Add Lambda permission
        try:
            lambda_client.add_permission(
                FunctionName=lambda_arn.split(':')[-1],
                StatementId=f'apigateway-{api_id}-{resource_id}-{http_method}',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com'
            )
        except:
            pass  # Permission might already exist
        
        # Create OPTIONS method for CORS
        try:
            apigateway.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            apigateway.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={'application/json': '{"statusCode": 200}'}
            )
            
            apigateway.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': True,
                    'method.response.header.Access-Control-Allow-Methods': True,
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            
            apigateway.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
        except:
            pass
        
    except Exception as e:
        print(f"    Warning: Error creating method {http_method}: {e}")

def main():
    """Main deployment function"""
    print("=" * 70)
    print("🚀 DEPLOYING SERVERLESS EKART STORE TO LOCALSTACK")
    print("=" * 70)
    print()
    
    try:
        # Create AWS clients
        print("Initializing AWS clients...")
        clients = create_aws_clients()
        print()
        
        # Create DynamoDB tables
        create_dynamodb_tables(clients['dynamodb'])
        print()
        
        # Create Cognito user pool
        user_pool_id, client_id = create_cognito_user_pool(clients['cognito'])
        print()
        
        # Create S3 buckets
        create_s3_buckets(clients['s3'])
        print()
        
        # Create Lambda role
        role_arn = create_lambda_role(clients['iam'])
        print()
        
        # Deploy Lambda functions
        lambda_functions = deploy_lambda_functions(
            clients['lambda_client'],
            role_arn,
            user_pool_id,
            client_id
        )
        print()
        
        # Create API Gateway
        api_id, api_url = create_api_gateway(
            clients['apigateway'],
            clients['lambda_client'],
            lambda_functions,
            user_pool_id
        )
        print()
        
        print("=" * 70)
        print("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("📋 DEPLOYMENT SUMMARY:")
        print(f"  • Region: {REGION}")
        print(f"  • Environment: {ENV}")
        print(f"  • Cognito User Pool ID: {user_pool_id}")
        print(f"  • Cognito Client ID: {client_id}")
        print(f"  • API Gateway ID: {api_id}")
        print(f"  • API Gateway URL: {api_url}")
        print()
        print("🎯 NEXT STEPS:")
        print("  1. Seed database: python scripts/seed.py")
        print("  2. Update frontend .env.local with API_URL")
        print("  3. Start frontend: cd frontend && npm run dev")
        print()
        print(f"  Frontend API URL: {api_url}")
        print(f"  Example: {api_url}/products")
        print()
        
        # Save configuration (preserve existing keys, update dynamic ones)
        _CFG.update({
            'api_url': api_url,
            'api_id': api_id,
            'user_pool_id': user_pool_id,
            'client_id': client_id,
            'region': REGION,
            'endpoint': ENDPOINT,
            'env': ENV,
            'lambda_endpoint': LAMBDA_ENDPOINT
        })
        with open(CONFIG_PATH, 'w') as f:
            json.dump(_CFG, f, indent=2)
        print(f"💾 Configuration saved to: {CONFIG_PATH}")
        print()

        # Update frontend .env.local
        env_path = PROJECT_ROOT / 'frontend' / '.env.local'
        env_content = f"""# EKart Store Frontend - Auto-generated Environment Configuration
# Generated from serverless-config.json

# API Gateway URL
NEXT_PUBLIC_API_URL={api_url}

# AWS Cognito Configuration
NEXT_PUBLIC_AWS_REGION={REGION}
NEXT_PUBLIC_USER_POOL_ID={user_pool_id}
NEXT_PUBLIC_CLIENT_ID={client_id}

# LocalStack Endpoint
NEXT_PUBLIC_AWS_ENDPOINT={ENDPOINT}

# Environment
NEXT_PUBLIC_ENV=development
"""
        with open(env_path, 'w') as env_file:
            env_file.write(env_content)
        print(f"🔧 Updated frontend .env.local: {env_path}")
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ DEPLOYMENT FAILED: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
