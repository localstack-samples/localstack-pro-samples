import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    Process new orders from API Gateway or SQS
    """
    print(f"Order processor invoked with event: {json.dumps(event)}")
    
    try:
        # Process order logic here
        order_data = json.loads(event.get('body', '{}')) if 'body' in event else event
        
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order processed successfully',
                'order_id': order_data.get('order_id', 'unknown'),
                'timestamp': datetime.utcnow().isoformat()
            })
        }
        
        return response
        
    except Exception as e:
        print(f"Error processing order: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
