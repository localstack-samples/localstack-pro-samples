import os
import time
import uuid
import datetime
import boto3

DYNAMODB_ENDPOINT = f'http://{os.environ["LOCALSTACK_HOSTNAME"]}:4569'
S3_ENDPOINT = f'http://{os.environ["LOCALSTACK_HOSTNAME"]}:4572'

DYNAMODB_TABLE = 'appRequests'
S3_BUCKET = 'archiveBucket'


def handleRequest(event, context=None):
    # simulate queueing delay
    time.sleep(5)
    print('handleRequest', event)
    # set request status to PROCESSING
    status = 'PROCESSING'
    setStatus(event['requestID'], status)
    # simulate processing delay
    time.sleep(4)
    return {
        'requestID': event['requestID'],
        'status': status
    }


def archiveResult(event, context=None):
    print('archiveResult', event)
    requestID = event['requestID']
    # put result onto S3
    s3 = getClient('s3')
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f'{requestID}/result.txt',
        Body=f'Archive result for request {requestID}'
    )
    # simulate processing delay
    time.sleep(3)
    # set request status to FINISHED
    setStatus(requestID, 'FINISHED')


def getClient(resource):
    endpoints = {
        'dynamodb': DYNAMODB_ENDPOINT,
        's3': S3_ENDPOINT
    }
    endpoint = endpoints.get(resource)
    return boto3.client(resource, endpoint_url=endpoint)


def setStatus(requestID, status):
    dynamodb = getClient('dynamodb')
    item = {
        'id': {'S': short_uid()},
        'requestID': {'S': requestID},
        'timestamp': {'N': str(now_utc())},
        'status': {'S': status}
    }
    dynamodb.put_item(TableName=DYNAMODB_TABLE, Item=item)


def now_utc():
    diff = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
    return int(diff.total_seconds() * 1000.0)


def short_uid():
    return str(uuid.uuid4())[0:8]
