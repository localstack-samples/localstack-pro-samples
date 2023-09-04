import os
import logging
import jsonpickle
import boto3
import uuid
import socket
import requests

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

EDGE_PORT = 4566


def short_uid() -> str:
    return str(uuid.uuid4())[0:8]


def lambda_handler(event, context):
    logger.info("## ENVIRONMENT VARIABLES\r" + jsonpickle.encode(dict(**os.environ)))
    logger.info("## EVENT\r" + jsonpickle.encode(event))
    logger.info("## CONTEXT\r" + jsonpickle.encode(context))

    host = "host.docker.internal"
    r = requests.get(f"http://{host}:2000")
    logger.info(r.text)

    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)

    serverAddressPort = (host, 20001)
    bufferSize = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)

    UDP_IP = "host.docker.internal"
    UDP_PORT = 2000
    MESSAGE = "Hello, LocalStack!"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

    xray_recorder.configure(
        sampling=False,
        context_missing="LOG_ERROR",
        # tcp emitter not implemented in XRay SDKs :(
        daemon_address="tcp:192.168.65.2:2000",
    )

    subsegment = xray_recorder.begin_subsegment("annotations")
    subsegment.put_annotation("id", 12345)
    xray_recorder.end_subsegment()

    endpoint_url = None
    if os.environ.get("LOCALSTACK_HOSTNAME"):
        protocol = "https" if os.environ.get("USE_SSL") else "http"
        endpoint_url = "{}://{}:{}".format(
            protocol, os.environ["LOCALSTACK_HOSTNAME"], EDGE_PORT
        )
    s3_client = boto3.client("s3", endpoint_url=endpoint_url, verify=False)

    bucket_name = f"mybucket-{short_uid()}"
    response = s3_client.create_bucket(Bucket=bucket_name)
    logger.info(response)
    return response
