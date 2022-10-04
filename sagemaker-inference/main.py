import json
import random

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


def deploy_model():
    # Put the Model into the correct bucket
    s3.create_bucket(Bucket=MODEL_BUCKET)
    s3.upload_file(MODEL_TAR, MODEL_BUCKET, f"{MODEL_NAME}.tar.gz")

    # Create the model in sagemaker
    sagemaker.create_model(ModelName=MODEL_NAME, ExecutionRoleArn=EXECUTION_ROLE_ARN,
                           PrimaryContainer={"Image": CONTAINER_IMAGE,
                                             "ModelDataUrl": f"s3://{MODEL_BUCKET}/{MODEL_NAME}.tar.gz"})
    sagemaker.create_endpoint_config(EndpointConfigName=CONFIG_NAME, ProductionVariants=[{
        "VariantName": "var1", "ModelName": MODEL_NAME, "InitialInstanceCount": 1, "InstanceType": "ml.m5.large"
    }])
    sagemaker.create_endpoint(EndpointName=ENDPOINT_NAME, EndpointConfigName=CONFIG_NAME)


def _get_input_dict():
    X, Y = mnist_to_numpy("data/mnist", train=False)
    mask = random.sample(range(X.shape[0]), 16)
    samples = X[mask]

    samples = normalize(samples.astype(np.float32), axis=(1, 2))
    return {
        "inputs": np.expand_dims(samples, axis=1).tolist()
    }

def _show_predictions(response):
    predictions = np.argmax(np.array(response, dtype=np.float32), axis=1).tolist()
    print(f"Predicted digits: {predictions}")


def inference_model_container():
    inputs = _get_input_dict()
    response = httpx.post("http://localhost.localstack.cloud:4510/invocations", json=inputs,
                          headers={"Content-Type": "application/json", "Accept": "application/json"})
    _show_predictions(json.loads(response.text))



def inference_model_boto3():
    print("inference...")
    sagemaker_runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, Body="", Accept="application/json")



if __name__ == '__main__':
    deploy_model()
    inference_model_container()
    # inference_model_boto3()
