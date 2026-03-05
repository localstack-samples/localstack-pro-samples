# SageMaker Model Inference

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | SageMaker, S3                       |
| Integrations | AWS SDK (boto3)                     |
| Categories   | ML; Inference                       |

## Introduction

A demo application illustrating how to host PyTorch ML models with SageMaker using LocalStack. The sample creates a SageMaker endpoint for an MNIST digit recognition model and demonstrates invocations both directly on the container and via the boto3 SDK.

> Note: This demo pulls AWS Deep Learning container images (~several GB). Pull the required image beforehand:
> ```bash
> docker pull 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.5.0-cpu-py3
> ```

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

The script creates an S3 bucket, uploads model data, creates a SageMaker endpoint, and invokes it to predict digit classes.

## License

This code is available under the Apache 2.0 license.
