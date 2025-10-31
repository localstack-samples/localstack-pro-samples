#!/usr/bin/env python3
"""
Test script for Serverless APIs
Tests all Lambda functions through API Gateway
"""
import requests
import json
import sys

# Load config
with open('serverless-config.json', 'r') as f:
    config = json.load(f)

API_URL = config['api_url']
BASE_URL = f"{API_URL}/api"

def print_test(name, status):
    """Print test result"""
    icon = "✅" if status else "❌"
    print(f"  {icon} {name}")
    return status

def test_products_api():
    """Test Products API"""
    print("\n📦 Testing Products API...")
    all_passed = True
    
    # GET all products
    r = requests.get(f"{BASE_URL}/products")
    all_passed &= print_test(f"GET /products - Status: {r.status_code}", r.status_code == 200)
    if r.status_code == 200:
        products = r.json()
        print(f"     Found {len(products)} products")
        if len(products) > 0:
            product_id = products[0]['product_id']
            
            # GET single product
            r = requests.get(f"{BASE_URL}/products/{product_id}")
            all_passed &= print_test(f"GET /products/{{id}} - Status: {r.status_code}", r.status_code == 200)
    
    return all_passed

def test_auth_api():
    """Test Authentication API"""
    print("\n🔐 Testing Authentication API...")
    all_passed = True
    
    # Register a new user
    user_data = {
        'email': 'testuser@example.com',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User',
        'user_type': 'buyer'
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    all_passed &= print_test(f"POST /auth/register - Status: {r.status_code}", r.status_code in [200, 400])
    
    # Login
    login_data = {
        'email': user_data['email'],
        'password': user_data['password']
    }
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    all_passed &= print_test(f"POST /auth/login - Status: {r.status_code}", r.status_code == 200)
    
    if r.status_code == 200:
        auth_data = r.json()
        token = auth_data.get('access_token')
        if token:
            print(f"     Got access token: {token[:50]}...")
            
            # Get user info
            headers = {'Authorization': f'Bearer {token}'}
            r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            all_passed &= print_test(f"GET /auth/me - Status: {r.status_code}", r.status_code == 200)
            
            return all_passed, token
    
    return all_passed, None

def test_cart_api(token):
    """Test Cart API"""
    print("\n🛒 Testing Cart API...")
    all_passed = True
    
    if not token:
        print("  ⚠️  Skipping cart tests (no auth token)")
        return True
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get cart (should be empty)
    r = requests.get(f"{BASE_URL}/cart", headers=headers)
    all_passed &= print_test(f"GET /cart - Status: {r.status_code}", r.status_code == 200)
    
    # Get a product to add to cart
    r = requests.get(f"{BASE_URL}/products")
    if r.status_code == 200:
        products = r.json()
        if len(products) > 0:
            product_id = products[0]['product_id']
            
            # Add to cart
            cart_item = {
                'product_id': product_id,
                'quantity': 2
            }
            r = requests.post(f"{BASE_URL}/cart/items", headers=headers, json=cart_item)
            all_passed &= print_test(f"POST /cart/items - Status: {r.status_code}", r.status_code == 200)
            
            # Update cart item
            update_data = {'quantity': 3}
            r = requests.put(f"{BASE_URL}/cart/items/{product_id}", headers=headers, json=update_data)
            all_passed &= print_test(f"PUT /cart/items/{{id}} - Status: {r.status_code}", r.status_code in [200, 405])
            
            # Get cart again (should have items)
            r = requests.get(f"{BASE_URL}/cart", headers=headers)
            all_passed &= print_test(f"GET /cart (with items) - Status: {r.status_code}", r.status_code == 200)
            if r.status_code == 200:
                cart = r.json()
                print(f"     Cart has {len(cart.get('items', []))} items")
    
    return all_passed

def test_cart_api_debug(token):
    """Test Cart API with debug output at each step"""
    print("\n🛒 [DEBUG] Testing Cart API (step-by-step)...")
    all_passed = True
    if not token:
        print("  [DEBUG] No auth token, skipping cart tests.")
        return True
    headers = {'Authorization': f'Bearer {token}'}

    print("  [DEBUG] Step 1: GET /cart (should be empty)")
    r = requests.get(f"{BASE_URL}/cart", headers=headers)
    print(f"    [DEBUG] Status: {r.status_code}, Response: {r.text}")
    all_passed &= print_test(f"GET /cart - Status: {r.status_code}", r.status_code == 200)

    print("  [DEBUG] Step 2: GET /products (to pick a product)")
    r = requests.get(f"{BASE_URL}/products")
    print(f"    [DEBUG] Status: {r.status_code}, Response: {r.text}")
    if r.status_code == 200:
        products = r.json()
        if len(products) > 0:
            product_id = products[0]['product_id']
            print(f"  [DEBUG] Step 3: POST /cart/items (add product {product_id})")
            cart_item = {
                'product_id': product_id,
                'quantity': 2
            }
            r = requests.post(f"{BASE_URL}/cart/items", headers=headers, json=cart_item)
            print(f"    [DEBUG] Status: {r.status_code}, Response: {r.text}")
            all_passed &= print_test(f"POST /cart/items - Status: {r.status_code}", r.status_code == 200)

            print(f"  [DEBUG] Step 4: PUT /cart/items/{{id}} (update quantity)")
            update_data = {'quantity': 3}
            r = requests.put(f"{BASE_URL}/cart/items/{product_id}", headers=headers, json=update_data)
            print(f"    [DEBUG] Status: {r.status_code}, Response: {r.text}")
            all_passed &= print_test(f"PUT /cart/items/{{id}} - Status: {r.status_code}", r.status_code in [200, 405])

            print("  [DEBUG] Step 5: GET /cart (should have items)")
            r = requests.get(f"{BASE_URL}/cart", headers=headers)
            print(f"    [DEBUG] Status: {r.status_code}, Response: {r.text}")
            all_passed &= print_test(f"GET /cart (with items) - Status: {r.status_code}", r.status_code == 200)
            if r.status_code == 200:
                cart = r.json()
                print(f"     [DEBUG] Cart has {len(cart.get('items', []))} items")
        else:
            print("  [DEBUG] No products found to add to cart.")
    else:
        print("  [DEBUG] Failed to fetch products.")
    return all_passed

def test_orders_api(token):
    """Test Orders API"""
    print("\n📋 Testing Orders API...")
    all_passed = True
    
    if not token:
        print("  ⚠️  Skipping orders tests (no auth token)")
        return True
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get orders (might be empty)
    r = requests.get(f"{BASE_URL}/orders", headers=headers)
    all_passed &= print_test(f"GET /orders - Status: {r.status_code}", r.status_code == 200)
    
    # Create order from cart
    order_data = {
        'shipping_address': {
            'street': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'zip_code': '12345',
            'country': 'USA'
        },
        'payment_method': 'card'
    }
    r = requests.post(f"{BASE_URL}/orders", headers=headers, json=order_data)
    all_passed &= print_test(f"POST /orders - Status: {r.status_code}", r.status_code in [200, 201, 400])
    
    return all_passed

def test_payments_api():
    """Test Payments API via LocalStack Stripe"""
    print("\n💳 Testing Payments API...")
    all_passed = True
    # Create a small test payment intent (e.g., $1.99 -> 199 cents)
    payload = {
        'amount': 199,
        'currency': 'usd',
        'description': 'Test checkout'
    }
    r = requests.post(f"{BASE_URL}/payments", json=payload)
    all_passed &= print_test(f"POST /payments - Status: {r.status_code}", r.status_code == 200)
    if r.status_code == 200:
        data = r.json()
        print(f"     Payment intent: {data.get('payment_intent_id')} status: {data.get('status')}")
    return all_passed

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 TESTING SERVERLESS EKART STORE APIs")
    print("=" * 70)
    print(f"\n🌐 API Gateway URL: {API_URL}")
    
    all_tests_passed = True
    
    # Test Products API (no auth required)
    all_tests_passed &= test_products_api()
    
    # Test Authentication API
    auth_passed, token = test_auth_api()
    all_tests_passed &= auth_passed
    
    # Test Cart API (requires auth)
    all_tests_passed &= test_cart_api(token)
    # Test Cart API with debug (requires auth)
    all_tests_passed &= test_cart_api_debug(token)
    
    # Test Orders API (requires auth)
    all_tests_passed &= test_orders_api(token)
    
    # Test Payments API (Stripe via LocalStack)
    all_tests_passed &= test_payments_api()
    
    # Summary
    print("\n" + "=" * 70)
    if all_tests_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    
    sys.exit(0 if all_tests_passed else 1)

if __name__ == '__main__':
    main()
