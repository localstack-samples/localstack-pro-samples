import json
import boto3
import os
import jwt
from decimal import Decimal
from datetime import datetime

def extract_user_from_token(event):
    """Extracts user ID from Authorization (JWT) header."""
    try:
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization") or headers.get("authorization")
        if not auth_header:
            return None
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        token = parts[1]
        decoded = jwt.decode(token, options={"verify_signature": False})  # Don't verify in dev!
        return decoded.get("sub") or decoded.get("username")
    except Exception as e:
        print("Token extraction error", str(e))
        return None

def decimal_default(obj):
    """JSON serializer for Decimal objects."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def cors_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps(body, default=decimal_default)
    }

endpoint_url = os.getenv("AWS_ENDPOINT_URL") or None
dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
CARTS_TABLE = os.getenv("CARTS_TABLE", "ekart-carts-dev")
PRODUCTS_TABLE = os.getenv("PRODUCTS_TABLE", "ekart-products-dev")

def get_cart(user_id):
    """Returns the user's cart."""
    try:
        table = dynamodb.Table(CARTS_TABLE)
        response = table.get_item(Key={"user_id": user_id})
        if "Item" not in response:
            return cors_response(200, {"user_id": user_id, "items": [], "total_amount": 0, "updated_at": datetime.utcnow().isoformat()})
        return cors_response(200, response["Item"])
    except Exception as e:
        print("Error getting cart", e)
        return cors_response(500, {"error": str(e)})

def add_to_cart(user_id, body):
    """Adds an item to the user's cart."""
    try:
        product_id = body['product_id']
        quantity = int(body.get("quantity", 1))
        product_table = dynamodb.Table(PRODUCTS_TABLE)
        prod_response = product_table.get_item(Key={"product_id": product_id})
        if "Item" not in prod_response:
            return cors_response(404, {"error": "Product not found"})
        product = prod_response["Item"]

        cart_table = dynamodb.Table(CARTS_TABLE)
        cart_response = cart_table.get_item(Key={"user_id": user_id})
        items = cart_response.get("Item", {}).get("items", [])

        # See if product already in cart
        for item in items:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            items.append({
                "product_id": product_id,
                "product_name": product.get("name") or product.get("title", "Unknown Product"),
                "price": Decimal(str(product.get("price"))),
                "quantity": int(quantity),
                "seller_id": product.get("seller_id")
            })

        total_amount = sum(Decimal(str(item["price"])) * Decimal(str(item["quantity"])) for item in items)
        cart = {
            "user_id": user_id,
            "items": items,
            "total_amount": Decimal(str(total_amount)),
            "updated_at": datetime.utcnow().isoformat()
        }
        cart_table.put_item(Item=cart)
        return cors_response(200, cart)
    except Exception as e:
        print("Error adding to cart", e)
        return cors_response(500, {"error": str(e)})

def update_cart_item(user_id, product_id, body):
    """Updates the quantity for a cart item."""
    try:
        quantity = int(body.get("quantity", 1))
        table = dynamodb.Table(CARTS_TABLE)
        response = table.get_item(Key={"user_id": user_id})
        if "Item" not in response:
            return cors_response(404, {"error": "Cart not found"})
        cart = response["Item"]
        items = cart.get("items", [])

        found = False
        for item in items:
            if item["product_id"] == product_id:
                if quantity == 0:
                    items.remove(item)
                else:
                    item["quantity"] = quantity
                found = True
                break
        if not found:
            return cors_response(404, {"error": "Item not found in cart"})

        total_amount = sum(Decimal(str(item["price"])) * Decimal(str(item["quantity"])) for item in items)
        cart["items"] = items
        cart["total_amount"] = Decimal(str(total_amount))
        cart["updated_at"] = datetime.utcnow().isoformat()
        table.put_item(Item=cart)
        return cors_response(200, cart)
    except Exception as e:
        print("Error updating cart", e)
        return cors_response(500, {"error": str(e)})

def remove_from_cart(user_id, product_id):
    """Removes a product from the cart."""
    try:
        table = dynamodb.Table(CARTS_TABLE)
        response = table.get_item(Key={"user_id": user_id})
        if "Item" not in response:
            return cors_response(404, {"error": "Cart not found"})
        cart = response["Item"]
        items = [item for item in cart.get("items", []) if item["product_id"] != product_id]
        cart["items"] = items
        cart["total_amount"] = Decimal(str(sum(Decimal(str(item["price"])) * Decimal(str(item["quantity"])) for item in items)))
        cart["updated_at"] = datetime.utcnow().isoformat()
        table.put_item(Item=cart)
        return cors_response(200, {"message": "Item removed from cart"})
    except Exception as e:
        print("Error removing from cart", e)
        return cors_response(500, {"error": str(e)})

def clear_cart(user_id):
    """Clears the user's cart."""
    try:
        table = dynamodb.Table(CARTS_TABLE)
        table.delete_item(Key={"user_id": user_id})
        return cors_response(200, {"message": "Cart cleared"})
    except Exception as e:
        print("Error clearing cart", e)
        return cors_response(500, {"error": str(e)})

def lambda_handler(event, context):
    print("Event", json.dumps(event))
    http_method = event.get("httpMethod", "")
    path = event.get("path", "")
    path_params = event.get("pathParameters") or {}
    product_id = path_params.get("id") or path_params.get("product_id")
    body = None
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {}

    if http_method == "OPTIONS":
        return cors_response(200, {})

    user_id = extract_user_from_token(event)
    if not user_id:
        return cors_response(401, {"error": "Authentication required"})

    if http_method == "GET" and "items" not in path:
        return get_cart(user_id)
    elif http_method == "POST" and "items" in path:
        return add_to_cart(user_id, body or {})
    elif http_method == "PUT" and product_id:
        return update_cart_item(user_id, product_id, body or {})
    elif http_method == "DELETE" and product_id:
        return remove_from_cart(user_id, product_id)
    elif http_method == "DELETE":
        return clear_cart(user_id)
    else:
        return cors_response(405, {"error": "Method not allowed"})
