#!/usr/bin/env python3

"""
Deploy AWS infrastructure to LocalStack using boto3 directly.
"""

import boto3
import json
from pathlib import Path
import time
import traceback

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'serverless-config.json'
with open(CONFIG_PATH, 'r') as _cfg_file:
    _CFG = json.load(_cfg_file)

ENDPOINT = _CFG.get('endpoint')
REGION = _CFG.get('region')
ENV = _CFG.get('env', 'dev')

def debug(msg):
    print(f"[deploy-infrastructure] {msg}")

def create_aws_clients():
    config = {
        'endpoint_url': ENDPOINT,
        'region_name': REGION,
        'aws_access_key_id': 'test',
        'aws_secret_access_key': 'test'
    }
    return {
        'dynamodb': boto3.client('dynamodb', **config),
        'cognito': boto3.client('cognito-idp', **config),
        's3': boto3.client('s3', **config)
    }

def create_dynamodb_tables(dynamodb):
    debug("Creating DynamoDB tables...")
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
            debug(f"✓ Created table: {table_config['TableName']}")
        except dynamodb.exceptions.ResourceInUseException:
            debug(f"⚠ Table already exists: {table_config['TableName']}")
        except Exception as e:
            debug(f"✗ Error creating table {table_config['TableName']}: {e}")

def create_cognito_user_pool(cognito):
    debug("Creating Cognito user pool...")
    try:
        response = cognito.create_user_pool(
            PoolName=f'ekart-users-{ENV}',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': False
                }
            },
            AutoVerifiedAttributes=['email']
        )
        user_pool_id = response['UserPool']['Id']
        debug(f"✓ Created user pool: {user_pool_id}")

        client_response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=f'ekart-client-{ENV}',
            ExplicitAuthFlows=['ALLOW_USER_SRP_AUTH', 'ALLOW_REFRESH_TOKEN_AUTH']
        )
        debug(f"✓ Created user pool client: {client_response['UserPoolClient']['ClientId']}")
        return user_pool_id
    except cognito.exceptions.ResourceConflictException:
        debug("⚠ User pool already exists")
        pools = cognito.list_user_pools(MaxResults=10)
        for pool in pools.get('UserPools', []):
            if pool['Name'] == f'ekart-users-{ENV}':
                return pool['Id']
    except Exception as e:
        debug(f"✗ Error creating user pool: {e}")
        traceback.print_exc()
    return None

def create_s3_buckets(s3):
    debug("Creating S3 buckets...")
    buckets = [f'ekart-product-images-{ENV}']
    for bucket_name in buckets:
        try:
            s3.create_bucket(Bucket=bucket_name)
            debug(f"✓ Created bucket: {bucket_name}")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            debug(f"⚠ Bucket already exists: {bucket_name}")
        except Exception as e:
            debug(f"✗ Error creating bucket {bucket_name}: {e}")

def main():
    debug("🚀 Deploying EKart Store infrastructure to LocalStack...\n")
    try:
        clients = create_aws_clients()
        create_dynamodb_tables(clients['dynamodb'])
        print()
        user_pool_id = create_cognito_user_pool(clients['cognito'])
        print()
        create_s3_buckets(clients['s3'])
        print()
        debug("✅ Infrastructure deployment completed successfully!")
        debug(f"User Pool ID: {user_pool_id}")
        debug(f"Region: {REGION}")
        debug(f"Environment: {ENV}")
    except Exception as e:
        debug(f"❌ Deployment failed: {e}")
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()

