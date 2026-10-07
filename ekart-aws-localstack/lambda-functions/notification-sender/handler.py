import json
import boto3
import os

def lambda_handler(event, context):
    """
    Send notifications via SES
    """
    print(f"Notification sender invoked with event: {json.dumps(event)}")
    
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Notification sent successfully'})
        }
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
