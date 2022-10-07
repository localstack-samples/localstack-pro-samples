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

sagemaker: SageMakerClient = boto3.client("sagemaker", endpoint_url=LOCALSTACK_ENDPOINT)
sagemaker_runtime: SageMakerRuntimeClient = boto3.client("sagemaker-runtime", endpoint_url=LOCALSTACK_ENDPOINT)
s3: S3Client = boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT)


def deploy_model(run_id: str = "0"):
    # Put the Model into the correct bucket
    s3.create_bucket(Bucket=f"{MODEL_BUCKET}-{run_id}")
    s3.upload_file(MODEL_TAR, f"{MODEL_BUCKET}-{run_id}", f"{MODEL_NAME}.tar.gz")

    # Create the model in sagemaker
    sagemaker.create_model(ModelName=f"{MODEL_NAME}-{run_id}", ExecutionRoleArn=EXECUTION_ROLE_ARN,
                           PrimaryContainer={"Image": CONTAINER_IMAGE,
                                             "ModelDataUrl": f"s3://{MODEL_BUCKET}-{run_id}/{MODEL_NAME}.tar.gz"})
    sagemaker.create_endpoint_config(EndpointConfigName=f"{CONFIG_NAME}-{run_id}", ProductionVariants=[{
        "VariantName": f"var-{run_id}", "ModelName": f"{MODEL_NAME}-{run_id}", "InitialInstanceCount": 1,
        "InstanceType": "ml.m5.large"
    }])
    sagemaker.create_endpoint(EndpointName=f"{ENDPOINT_NAME}-{run_id}", EndpointConfigName=f"{CONFIG_NAME}-{run_id}")


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
    response = httpx.post(f"http://localhost.localstack.cloud:{port}/invocations", json=inputs,
                          headers={"Content-Type": "application/json", "Accept": "application/json"})
    _show_predictions(json.loads(response.text))


def inference_model_boto3(run_id: str = "0"):
    inputs = _get_input_dict()
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
    # wait some time to avoid connection resets in log output
    # -> not essential as the container spins up quickly enough within the retries of boto
    time.sleep(2)
    inference_model_boto3(test_run)
    inference_model_container(test_run)
