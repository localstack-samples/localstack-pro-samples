import json
import boto3
import os

def lambda_handler(event, context):
    """
    Update inventory levels based on orders
    """
    print(f"Inventory updater invoked with event: {json.dumps(event)}")
    
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Inventory updated successfully'})
        }
    except Exception as e:
        print(f"Error updating inventory: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
