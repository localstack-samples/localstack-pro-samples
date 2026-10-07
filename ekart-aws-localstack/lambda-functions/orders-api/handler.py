"""
Lambda function for Orders API
Handles: GET /orders, GET /orders/{id}, POST /orders, PUT /orders/{id}/status
"""
import json
import boto3
import os
import uuid
import jwt
from decimal import Decimal
from datetime import datetime

# AWS clients
endpoint_url = os.getenv('AWS_ENDPOINT_URL') or None
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
ORDERS_TABLE = os.getenv('ORDERS_TABLE', 'ekart-orders-dev')
CARTS_TABLE = os.getenv('CARTS_TABLE', 'ekart-carts-dev')
PRODUCTS_TABLE = os.getenv('PRODUCTS_TABLE', 'ekart-products-dev')

def extract_user_from_token(event):
    """Extract user ID and user type from JWT token"""
    try:
        # Get authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header:
            return None, None
        
        # Extract token from "Bearer <token>"
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None, None
        
        token = parts[1]
        
        # Decode token without verification (LocalStack doesn't have proper keys)
        # In production, you should verify the token signature
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Extract user ID and user type from claims
        user_id = decoded.get('sub') or decoded.get('username')
        user_type = decoded.get('custom:user_type', 'customer')
        return user_id, user_type
        
    except Exception as e:
        print(f"Token extraction error: {str(e)}")
        return None, None

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
            'Access-Control-Allow-Methods': 'GET,POST,PUT,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def get_orders(user_id, user_type):
    """Get orders for user (buyer or seller)"""
    try:
        table = dynamodb.Table(ORDERS_TABLE)
        
        # Query based on user type
        if user_type == 'seller':
            response = table.query(
                IndexName='seller-index',
                KeyConditionExpression='seller_id = :seller_id',
                ExpressionAttributeValues={':seller_id': user_id}
            )
        else:
            response = table.query(
                IndexName='buyer-index',
                KeyConditionExpression='buyer_id = :buyer_id',
                ExpressionAttributeValues={':buyer_id': user_id}
            )
        
        orders = response.get('Items', [])
        return cors_response(200, orders)
    except Exception as e:
        print(f"Error getting orders: {e}")
        return cors_response(500, {'error': str(e)})

def get_order_by_id(order_id, user_id):
    """Get single order by ID"""
    try:
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Order not found'})
        
        order = response['Item']
        
        # Verify user has access to this order
        if order['buyer_id'] != user_id and order.get('seller_id') != user_id:
            return cors_response(403, {'error': 'Not authorized to view this order'})
        
        return cors_response(200, order)
    except Exception as e:
        print(f"Error getting order: {e}")
        return cors_response(500, {'error': str(e)})

def create_order(user_id, body):
    """Create new order from cart"""
    try:
        # Get user's cart
        carts_table = dynamodb.Table(CARTS_TABLE)
        cart_response = carts_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in cart_response or not cart_response['Item'].get('items'):
            return cors_response(400, {'error': 'Cart is empty'})
        
        cart = cart_response['Item']
        items = cart['items']
        
        # Get shipping info from body
        shipping_address = body.get('shipping_address', {})
        payment_method = body.get('payment_method', 'card')
        
        # Group items by seller
        orders_by_seller = {}
        for item in items:
            seller_id = item['seller_id']
            if seller_id not in orders_by_seller:
                orders_by_seller[seller_id] = []
            orders_by_seller[seller_id].append(item)
        
        # Create separate orders for each seller
        created_orders = []
        orders_table = dynamodb.Table(ORDERS_TABLE)
        
        for seller_id, seller_items in orders_by_seller.items():
            order_id = str(uuid.uuid4())
            total = sum(Decimal(str(item['price'])) * item['quantity'] for item in seller_items)
            now = datetime.utcnow().isoformat()
            
            order = {
                'order_id': order_id,
                'buyer_id': user_id,
                'seller_id': seller_id,
                'items': seller_items,
                'total_amount': total,
                'status': 'pending',
                'payment_method': payment_method,
                'payment_status': 'pending',
                'shipping_address': shipping_address,
                'created_at': now,
                'updated_at': now
            }
            
            orders_table.put_item(Item=order)
            created_orders.append(order)
        
        # Clear cart
        carts_table.delete_item(Key={'user_id': user_id})
        
        return cors_response(201, {
            'message': 'Orders created successfully',
            'orders': created_orders
        })
        
    except Exception as e:
        print(f"Error creating order: {e}")
        return cors_response(500, {'error': str(e)})

def update_order_status(order_id, user_id, body):
    """Update order status (seller only)"""
    try:
        status = body.get('status')
        
        if status not in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
            return cors_response(400, {'error': 'Invalid status'})
        
        # Get order
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Order not found'})
        
        order = response['Item']
        
        # Verify seller owns this order
        if order.get('seller_id') != user_id:
            return cors_response(403, {'error': 'Not authorized to update this order'})
        
        # Update status
        table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET #status = :status, updated_at = :updated',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': status,
                ':updated': datetime.utcnow().isoformat()
            }
        )
        
        return cors_response(200, {'message': 'Order status updated', 'status': status})
        
    except Exception as e:
        print(f"Error updating order: {e}")
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    """
    Main Lambda handler for Orders API
    """
    print(f"Event: {json.dumps(event)}")
    
    try:
        http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method'))
        path = event.get('path', '')
        
        # Handle OPTIONS for CORS
        if http_method == 'OPTIONS':
            return cors_response(200, {})
        
        # Extract user from JWT token
        user_id, user_type = extract_user_from_token(event)
        
        if not user_id:
            return cors_response(401, {'error': 'Authentication required'})
        
        # Parse path parameters
        path_params = event.get('pathParameters') or {}
        order_id = path_params.get('id') or path_params.get('order_id')
        
        # Parse body
        body = {}
        if event.get('body'):
            body = json.loads(event['body'])
        
        # Route to appropriate handler
        if http_method == 'GET':
            if order_id:
                return get_order_by_id(order_id, user_id)
            else:
                return get_orders(user_id, user_type)
        
        elif http_method == 'POST' and not order_id:
            return create_order(user_id, body)
        
        elif http_method == 'PUT' and order_id and '/status' in path:
            return update_order_status(order_id, user_id, body)
        
        else:
            return cors_response(405, {'error': 'Method not allowed'})
            
    except Exception as e:
        print(f"Lambda handler error: {e}")
        return cors_response(500, {'error': str(e)})
