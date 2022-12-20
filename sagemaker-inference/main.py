import json
import random
import time

import boto3
import httpx
import numpy as np
from mypy_boto3_s3 import S3Client
from mypy_boto3_sagemaker import SageMakerClient
from mypy_boto3_sagemaker_runtime import SageMakerRuntimeClient

from mnist import mnist_to_numpy, normalize

LOCALSTACK_ENDPOINT = "http://localhost.localstack.cloud:4566"
MODEL_BUCKET = "models"
MODEL_TAR = "./data/model.tar.gz"
MODEL_NAME = "sample"
CONFIG_NAME = "sample-cf"
ENDPOINT_NAME = "sample-ep"
CONTAINER_IMAGE = "763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.5.0-cpu-py3"
EXECUTION_ROLE_ARN = "arn:aws:iam::0000000000000:role/sagemaker-role"

sagemaker: SageMakerClient = boto3.client("sagemaker", endpoint_url=LOCALSTACK_ENDPOINT, region_name="us-east-1")
sagemaker_runtime: SageMakerRuntimeClient = boto3.client("sagemaker-runtime", endpoint_url=LOCALSTACK_ENDPOINT,
                                                         region_name="us-east-1")
s3: S3Client = boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name="us-east-1")


def deploy_model(run_id: str = "0"):
    # Put the Model into the correct bucket
    print("Creating bucket...")
    s3.create_bucket(Bucket=f"{MODEL_BUCKET}-{run_id}")
    print("Uploading model data to bucket...")
    s3.upload_file(MODEL_TAR, f"{MODEL_BUCKET}-{run_id}", f"{MODEL_NAME}.tar.gz")

    # Create the model in sagemaker
    print("Creating model in SageMaker...")
    sagemaker.create_model(ModelName=f"{MODEL_NAME}-{run_id}", ExecutionRoleArn=EXECUTION_ROLE_ARN,
                           PrimaryContainer={"Image": CONTAINER_IMAGE,
                                             "ModelDataUrl": f"s3://{MODEL_BUCKET}-{run_id}/{MODEL_NAME}.tar.gz"})
    print("Adding endpoint configuration...")
    sagemaker.create_endpoint_config(EndpointConfigName=f"{CONFIG_NAME}-{run_id}", ProductionVariants=[{
        "VariantName": f"var-{run_id}", "ModelName": f"{MODEL_NAME}-{run_id}", "InitialInstanceCount": 1,
        "InstanceType": "ml.m5.large"
    }])
    print("Creating endpoint...")
    sagemaker.create_endpoint(EndpointName=f"{ENDPOINT_NAME}-{run_id}", EndpointConfigName=f"{CONFIG_NAME}-{run_id}")


def await_endpoint(run_id: str = "0", wait: float = 0.5, max_retries=10, _retries: int = 0):
    print("Checking endpoint status...")
    status = sagemaker.describe_endpoint(EndpointName=f"{ENDPOINT_NAME}-{run_id}")["EndpointStatus"]
    if status == "InService":
        print("Endpoint ready!")
        return True
    if _retries == max_retries:
        print("Endpoint unreachable!")
        return False
    print("Endpoint not ready - waiting...")
    time.sleep(wait)
    return await_endpoint(run_id, wait * 2, max_retries, _retries + 1)


def _get_input_dict():
    X, Y = mnist_to_numpy("data/mnist", train=False)
    mask = random.sample(range(X.shape[0]), 2)
    samples = X[mask]

    samples = normalize(samples.astype(np.float32), axis=(1, 2))
    return {
        "inputs": np.expand_dims(samples, axis=1).tolist()
    }


def _show_predictions(response):
    predictions = np.argmax(np.array(response, dtype=np.float32), axis=1).tolist()
    print(f"Predicted digits: {predictions}")


def inference_model_container(run_id: str = "0"):
    ep = sagemaker.describe_endpoint(EndpointName=f"{ENDPOINT_NAME}-{run_id}")
    arn = ep["EndpointArn"]
    tag_list = sagemaker.list_tags(ResourceArn=arn)
    port = "4510"
    for tag in tag_list["Tags"]:
        if tag["Key"] == "_LS_ENDPOINT_PORT_":
            port = tag["Value"]
    inputs = _get_input_dict()
    print("Invoking endpoint directly...")
    response = httpx.post(f"http://localhost.localstack.cloud:{port}/invocations", json=inputs,
                          headers={"Content-Type": "application/json", "Accept": "application/json"})
    _show_predictions(json.loads(response.text))


def inference_model_boto3(run_id: str = "0"):
    inputs = _get_input_dict()
    print("Invoking via boto...")
    response = sagemaker_runtime.invoke_endpoint(EndpointName=f"{ENDPOINT_NAME}-{run_id}", Body=json.dumps(inputs),
                                                 Accept="application/json",
                                                 ContentType="application/json")
    _show_predictions(json.loads(response["Body"].read()))


def _short_uid():
    import uuid

    return str(uuid.uuid4())[:8]


if __name__ == '__main__':
    test_run = _short_uid()
    deploy_model(test_run)
    if not await_endpoint(test_run):
        exit(-1)
    inference_model_boto3(test_run)
    inference_model_container(test_run)
