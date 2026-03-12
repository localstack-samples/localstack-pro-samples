# SageMaker Model Inference

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | SageMaker, S3                       |
| Integrations | AWS SDK (boto3)                     |
| Categories   | ML; Inference                       |

## Introduction

A demo application illustrating how to host PyTorch ML models with SageMaker using LocalStack. The sample creates a SageMaker endpoint for an MNIST digit recognition model and demonstrates invocations both directly on the container and via the boto3 SDK.

### Obtain the Deep Learning Image

Before running this example, set up your Docker client to pull AWS Deep Learning images ([more info](https://github.com/aws/deep-learning-containers/blob/master/available_images.md)):

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com
```

Because the images tend to be heavy (multiple GB), pull them beforehand:

```bash
docker pull 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.5.0-cpu-py3
```

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [Python 3.8+](https://www.python.org/downloads/)

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Start LocalStack

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script creates an S3 bucket, uploads model data, creates a SageMaker endpoint, and invokes it to predict digit classes. You should see output similar to:

```
Creating bucket...
Uploading model data to bucket...
Creating model in SageMaker...
Adding endpoint configuration...
Creating endpoint...
Checking endpoint status...
Endpoint not ready - waiting...
Checking endpoint status...
Endpoint ready!
Invoking via boto...
Predicted digits: [7, 3]
Invoking endpoint directly...
Predicted digits: [2, 6]
```

To try out the serverless run, remove the comment in `main.py` and run the example again.

## License

This code is available under the Apache 2.0 license.
