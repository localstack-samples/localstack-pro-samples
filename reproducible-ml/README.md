# Reproducible ML with Lambda and S3

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, S3                          |
| Integrations | AWS CLI                             |
| Categories   | ML; Serverless                      |

## Introduction

A demo application illustrating how to train, save, and evaluate a scikit-learn machine learning model using Lambda and S3 with LocalStack. A training Lambda function trains a digit recognition model and stores it in S3, while a second Lambda function downloads the model and runs predictions.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)

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
make start
```

## Run the application

```bash
make run
```

The script trains a scikit-learn digit recognition model via a Lambda function, stores it in S3, then invokes a second Lambda to download and evaluate the model.

## License

This code is available under the Apache 2.0 license.
