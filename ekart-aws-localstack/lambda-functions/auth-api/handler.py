"""
Lambda function for Authentication API with AWS Cognito
Handles: POST /auth/register, POST /auth/login, POST /auth/refresh, GET /auth/me
"""
import json
import boto3
import os
import hmac
import hashlib
import base64

# AWS clients
endpoint_url = os.getenv('AWS_ENDPOINT_URL') or None
cognito = boto3.client('cognito-idp', endpoint_url=endpoint_url)
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)

USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
USERS_TABLE = os.getenv('USERS_TABLE', 'ekart-users-dev')

def get_secret_hash(username):
    """Calculate SECRET_HASH for Cognito"""
    if not CLIENT_SECRET:
        return None
    message = bytes(username + CLIENT_ID, 'utf-8')
    secret = bytes(CLIENT_SECRET, 'utf-8')
    dig = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def cors_response(status_code, body):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }

def register_user(body):
    """Register a new user in Cognito and DynamoDB"""
    try:
        email = body['email']
        password = body['password']
        first_name = body.get('first_name', '')
        last_name = body.get('last_name', '')
        user_type = body.get('user_type', 'customer')
        
        # Prepare Cognito sign up parameters
        params = {
            'ClientId': CLIENT_ID,
            'Username': email,
            'Password': password,
            'UserAttributes': [
                {'Name': 'email', 'Value': email},
                {'Name': 'custom:user_type', 'Value': user_type},
                {'Name': 'custom:first_name', 'Value': first_name},
                {'Name': 'custom:last_name', 'Value': last_name}
            ]
        }
        
        # Add SECRET_HASH if client secret exists
        secret_hash = get_secret_hash(email)
        if secret_hash:
            params['SecretHash'] = secret_hash
        
        # Register in Cognito
        response = cognito.sign_up(**params)
        user_sub = response['UserSub']
        
        # Auto-confirm user in LocalStack (for dev/testing)
        # Always auto-confirm in LocalStack since we don't have email service
        try:
            cognito.admin_confirm_sign_up(
                UserPoolId=USER_POOL_ID,
                Username=email
            )
        except Exception as e:
            print(f"Auto-confirm failed (may not be needed): {str(e)}")
            pass
        
        # Store additional user data in DynamoDB
        from datetime import datetime
        table = dynamodb.Table(USERS_TABLE)
        user_data = {
            'user_id': user_sub,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone': body.get('phone', ''),
            'user_type': user_type,
            'is_active': True,
            'is_verified': True,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        table.put_item(Item=user_data)
        
        # Automatically log in the user
        auth_params = {
            'USERNAME': email,
            'PASSWORD': password
        }
        if secret_hash:
            auth_params['SECRET_HASH'] = secret_hash
        
        auth_response = cognito.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters=auth_params
        )
        
        return cors_response(200, {
            'access_token': auth_response['AuthenticationResult']['AccessToken'],
            'id_token': auth_response['AuthenticationResult']['IdToken'],
            'refresh_token': auth_response['AuthenticationResult']['RefreshToken'],
            'token_type': 'Bearer',
            'user_id': user_sub,
            'email': email,
            'user_type': user_type
        })
        
    except cognito.exceptions.UsernameExistsException:
        return cors_response(400, {'error': 'Email already registered'})
    except cognito.exceptions.InvalidPasswordException as e:
        return cors_response(400, {'error': f'Invalid password: {str(e)}'})
    except Exception as e:
        print(f"Registration error: {e}")
        return cors_response(500, {'error': str(e)})

def login_user(body):
    """Login user with Cognito"""
    try:
        email = body['email']
        password = body['password']
        
        # Prepare auth parameters
        auth_params = {
            'USERNAME': email,
            'PASSWORD': password
        }
        
        # Add SECRET_HASH if client secret exists
        secret_hash = get_secret_hash(email)
        if secret_hash:
            auth_params['SECRET_HASH'] = secret_hash
        
        # Authenticate with Cognito
        response = cognito.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters=auth_params
        )
        
        # Get user attributes
        access_token = response['AuthenticationResult']['AccessToken']
        user_info = cognito.get_user(AccessToken=access_token)
        
        # Extract user attributes
        attributes = {attr['Name']: attr['Value'] for attr in user_info['UserAttributes']}
        user_type = attributes.get('custom:user_type', 'customer')
        
        return cors_response(200, {
            'access_token': access_token,
            'id_token': response['AuthenticationResult']['IdToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken'],
            'token_type': 'Bearer',
            'user_id': user_info['Username'],
            'email': attributes.get('email'),
            'user_type': user_type
        })
        
    except cognito.exceptions.NotAuthorizedException:
        return cors_response(401, {'error': 'Invalid email or password'})
    except cognito.exceptions.UserNotFoundException:
        return cors_response(401, {'error': 'Invalid email or password'})
    except Exception as e:
        print(f"Login error: {e}")
        return cors_response(500, {'error': str(e)})

def refresh_token(body):
    """Refresh access token"""
    try:
        refresh_token = body['refresh_token']
        
        # Prepare auth parameters
        auth_params = {
            'REFRESH_TOKEN': refresh_token
        }
        
        # Note: For refresh token, we may need the username
        # This is a simplified version
        response = cognito.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters=auth_params
        )
        
        return cors_response(200, {
            'access_token': response['AuthenticationResult']['AccessToken'],
            'id_token': response['AuthenticationResult']['IdToken'],
            'token_type': 'Bearer'
        })
        
    except Exception as e:
        print(f"Token refresh error: {e}")
        return cors_response(401, {'error': 'Invalid refresh token'})

def get_current_user(event):
    """Get current user info from token"""
    try:
        # Extract token from Authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return cors_response(401, {'error': 'No token provided'})
        
        access_token = auth_header.replace('Bearer ', '')
        
        # Get user from Cognito
        user_info = cognito.get_user(AccessToken=access_token)
        
        # Extract attributes
        attributes = {attr['Name']: attr['Value'] for attr in user_info['UserAttributes']}
        
        # Get additional data from DynamoDB
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'user_id': user_info['Username']})
        
        user_data = response.get('Item', {})
        
        return cors_response(200, {
            'user_id': user_info['Username'],
            'email': attributes.get('email'),
            'user_type': attributes.get('custom:user_type', user_data.get('user_type', 'customer')),
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'phone': user_data.get('phone', ''),
            'is_verified': user_data.get('is_verified', True)
        })
        
    except cognito.exceptions.NotAuthorizedException:
        return cors_response(401, {'error': 'Invalid or expired token'})
    except Exception as e:
        print(f"Get user error: {e}")
        return cors_response(401, {'error': str(e)})

def lambda_handler(event, context):
    """
    Main Lambda handler for Auth API
    Routes based on HTTP method and path
    """
    print(f"Event: {json.dumps(event)}")
    
    try:
        http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method'))
        path = event.get('path', '').rstrip('/')
        
        # Handle OPTIONS for CORS
        if http_method == 'OPTIONS':
            return cors_response(200, {})
        
        # Parse body
        body = {}
        if event.get('body'):
            body = json.loads(event['body'])
        
        # Route to appropriate handler
        if path.endswith('/register') and http_method == 'POST':
            return register_user(body)
        
        elif path.endswith('/login') and http_method == 'POST':
            return login_user(body)
        
        elif path.endswith('/refresh') and http_method == 'POST':
            return refresh_token(body)
        
        elif path.endswith('/me') and http_method == 'GET':
            return get_current_user(event)
        
        else:
            return cors_response(404, {'error': 'Endpoint not found'})
            
    except Exception as e:
        print(f"Lambda handler error: {e}")
        return cors_response(500, {'error': str(e)})
