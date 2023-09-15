import os
import logging
import jsonpickle
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

client = boto3.client("lambda")
client.get_account_settings()

def lambda_handler(event, context):
    logger.info("## ENVIRONMENT VARIABLES\r" + jsonpickle.encode(dict(**os.environ)))
    logger.info("## EVENT\r" + jsonpickle.encode(event))
    logger.info("## CONTEXT\r" + jsonpickle.encode(context))

    # Automatic tracing of patched boto clients
    response = client.get_account_settings()

    # Custom tracing using the AWS X-Ray SDK
    subsegment = xray_recorder.begin_subsegment("annotations")
    subsegment.put_annotation("custom_annotation", 12345)
    xray_recorder.end_subsegment()

    return response["AccountUsage"]
