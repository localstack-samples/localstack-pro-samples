import json
import os
import base64
from urllib import request, parse, error

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }

def create_payment_intent(amount_cents: int, currency: str):
    base_url = os.getenv('STRIPE_BASE_URL')
    api_key = os.getenv('STRIPE_API_KEY')
    if not base_url or not api_key:
        raise RuntimeError('Stripe configuration missing')

    url = f"{base_url}/v1/payment_intents"
    data = parse.urlencode({
        'amount': str(amount_cents),
        'currency': currency
    }).encode('utf-8')

    # Basic auth with API key
    auth_token = base64.b64encode(f"{api_key}:".encode('utf-8')).decode('utf-8')
    req = request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Basic {auth_token}')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    try:
        with request.urlopen(req, timeout=10) as resp:
            payload = resp.read().decode('utf-8')
            return json.loads(payload)
    except error.HTTPError as e:
        detail = e.read().decode('utf-8') if e.fp else ''
        raise RuntimeError(f"Stripe error {e.code}: {detail}")

def lambda_handler(event, context):
    print(f"Payment processor invoked with event: {json.dumps(event)}")
    method = event.get('httpMethod')
    if method == 'OPTIONS':
        return cors_response(200, {})

    try:
        body = {}
        if event.get('body'):
            body = json.loads(event['body'])
        amount = int(body.get('amount', 0))
        currency = body.get('currency', 'usd')
        if amount <= 0:
            return cors_response(400, {'error': 'Invalid amount'})

        intent = create_payment_intent(amount, currency)
        # Return client_secret for frontend confirmation if needed
        return cors_response(200, {
            'payment_intent_id': intent.get('id'),
            'client_secret': intent.get('client_secret'),
            'status': intent.get('status')
        })
    except Exception as e:
        print(f"Error processing payment: {str(e)}")
        return cors_response(500, {'error': str(e)})
