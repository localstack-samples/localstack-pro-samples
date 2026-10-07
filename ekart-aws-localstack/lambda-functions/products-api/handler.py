"""
Lambda function for Products API
Handles: GET /products, GET /products/{id}, POST /products, PUT /products/{id}, DELETE /products/{id}
"""
import json
import boto3
import os
from decimal import Decimal
from datetime import datetime

# AWS clients
endpoint_url = os.getenv('AWS_ENDPOINT_URL') or None
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
PRODUCTS_TABLE = os.getenv('PRODUCTS_TABLE', 'ekart-products-dev')

def decimal_default(obj):
    """JSON serializer for Decimal objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def cors_response(status_code, body):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def get_all_products(query_params):
    """Get all products with optional filtering"""
    try:
        table = dynamodb.Table(PRODUCTS_TABLE)
        
        # Get query parameters
        category = query_params.get('category')
        seller_id = query_params.get('seller_id')
        search = query_params.get('search', '').lower()
        
        # Scan or query based on parameters
        if category:
            response = table.query(
                IndexName='category-index',
                KeyConditionExpression='category = :category',
                ExpressionAttributeValues={':category': category}
            )
        elif seller_id:
            response = table.query(
                IndexName='seller-index',
                KeyConditionExpression='seller_id = :seller_id',
                ExpressionAttributeValues={':seller_id': seller_id}
            )
        else:
            response = table.scan()
        
        items = response.get('Items', [])
        
        # Apply search filter if provided
        if search:
            items = [
                item for item in items
                if search in item.get('name', '').lower() or 
                   search in item.get('description', '').lower()
            ]
        
        return cors_response(200, items)
    except Exception as e:
        print(f"Error getting products: {e}")
        return cors_response(500, {'error': str(e)})

def get_product_by_id(product_id):
    """Get single product by ID"""
    try:
        table = dynamodb.Table(PRODUCTS_TABLE)
        response = table.get_item(Key={'product_id': product_id})
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Product not found'})
        
        return cors_response(200, response['Item'])
    except Exception as e:
        print(f"Error getting product: {e}")
        return cors_response(500, {'error': str(e)})

def create_product(body, user_id):
    """Create new product (seller only)"""
    try:
        import uuid
        table = dynamodb.Table(PRODUCTS_TABLE)
        
        product_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        product = {
            'product_id': product_id,
            'seller_id': user_id,
            'name': body['name'],
            'description': body['description'],
            'price': Decimal(str(body['price'])),
            'category': body['category'],
            'stock_quantity': int(body.get('stock_quantity', 0)),
            'image_url': body.get('image_url', ''),
            'is_active': True,
            'created_at': now,
            'updated_at': now
        }
        
        table.put_item(Item=product)
        return cors_response(201, product)
    except Exception as e:
        print(f"Error creating product: {e}")
        return cors_response(500, {'error': str(e)})

def update_product(product_id, body, user_id):
    """Update product (seller only - owner check required)"""
    try:
        table = dynamodb.Table(PRODUCTS_TABLE)
        
        # First check if product exists and user is the seller
        response = table.get_item(Key={'product_id': product_id})
        if 'Item' not in response:
            return cors_response(404, {'error': 'Product not found'})
        
        if response['Item']['seller_id'] != user_id:
            return cors_response(403, {'error': 'Not authorized to update this product'})
        
        # Update product
        update_expr = "SET "
        expr_values = {}
        expr_names = {}
        
        if 'name' in body:
            update_expr += "#n = :name, "
            expr_values[':name'] = body['name']
            expr_names['#n'] = 'name'
        if 'description' in body:
            update_expr += "description = :desc, "
            expr_values[':desc'] = body['description']
        if 'price' in body:
            update_expr += "price = :price, "
            expr_values[':price'] = Decimal(str(body['price']))
        if 'stock_quantity' in body:
            update_expr += "stock_quantity = :stock, "
            expr_values[':stock'] = int(body['stock_quantity'])
        if 'category' in body:
            update_expr += "category = :category, "
            expr_values[':category'] = body['category']
        if 'image_url' in body:
            update_expr += "image_url = :image, "
            expr_values[':image'] = body['image_url']
        
        update_expr += "updated_at = :updated"
        expr_values[':updated'] = datetime.utcnow().isoformat()
        
        kwargs = {
            'Key': {'product_id': product_id},
            'UpdateExpression': update_expr,
            'ExpressionAttributeValues': expr_values,
            'ReturnValues': 'ALL_NEW'
        }
        
        if expr_names:
            kwargs['ExpressionAttributeNames'] = expr_names
        
        response = table.update_item(**kwargs)
        return cors_response(200, response['Attributes'])
    except Exception as e:
        print(f"Error updating product: {e}")
        return cors_response(500, {'error': str(e)})

def delete_product(product_id, user_id):
    """Delete product (seller only - owner check required)"""
    try:
        table = dynamodb.Table(PRODUCTS_TABLE)
        
        # Check ownership
        response = table.get_item(Key={'product_id': product_id})
        if 'Item' not in response:
            return cors_response(404, {'error': 'Product not found'})
        
        if response['Item']['seller_id'] != user_id:
            return cors_response(403, {'error': 'Not authorized to delete this product'})
        
        table.delete_item(Key={'product_id': product_id})
        return cors_response(200, {'message': 'Product deleted successfully'})
    except Exception as e:
        print(f"Error deleting product: {e}")
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    """
    Main Lambda handler for Products API
    Routes based on HTTP method and path
    """
    print(f"Event: {json.dumps(event)}")
    
    try:
        http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method'))
        path = event.get('path', '')
        query_params = event.get('queryStringParameters') or {}
        
        # Handle OPTIONS for CORS
        if http_method == 'OPTIONS':
            return cors_response(200, {})
        
        # Extract user from authorizer context (if authenticated)
        request_context = event.get('requestContext', {})
        authorizer = request_context.get('authorizer', {})
        user_id = authorizer.get('claims', {}).get('sub') or authorizer.get('principalId')
        
        # Parse path parameters
        path_params = event.get('pathParameters') or {}
        product_id = path_params.get('id') or path_params.get('product_id')
        
        # Parse body for POST/PUT
        body = {}
        if event.get('body'):
            body = json.loads(event['body'])
        
        # Route to appropriate handler
        if http_method == 'GET':
            if product_id:
                return get_product_by_id(product_id)
            else:
                return get_all_products(query_params)
        
        elif http_method == 'POST':
            if not user_id:
                return cors_response(401, {'error': 'Authentication required'})
            return create_product(body, user_id)
        
        elif http_method == 'PUT':
            if not user_id:
                return cors_response(401, {'error': 'Authentication required'})
            if not product_id:
                return cors_response(400, {'error': 'Product ID required'})
            return update_product(product_id, body, user_id)
        
        elif http_method == 'DELETE':
            if not user_id:
                return cors_response(401, {'error': 'Authentication required'})
            if not product_id:
                return cors_response(400, {'error': 'Product ID required'})
            return delete_product(product_id, user_id)
        
        else:
            return cors_response(405, {'error': 'Method not allowed'})
            
    except Exception as e:
        print(f"Lambda handler error: {e}")
        return cors_response(500, {'error': str(e)})
