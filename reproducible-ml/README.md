# Reproducible ML with Lambda and S3

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, S3                          |
| Integrations | AWS CLI                             |
| Categories   | ML; Serverless                      |

## Introduction

A demo application illustrating how to train, save, and evaluate a scikit-learn machine learning model using Lambda and S3 with LocalStack. A training Lambda function trains a digit recognition model and stores it in S3, while a second Lambda function downloads the model and runs predictions.

In this demo application, we will train a simple machine-learning model that recognizes handwritten digits on an image. We will use the following services:

- An S3 bucket to host the training data;
- A Lambda function to train and save the model to an S3 bucket;
- A Lambda layer that contains the dependencies for the training code;
- A second Lambda function to download the saved model and perform a prediction with it.

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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script trains a scikit-learn digit recognition model via a Lambda function, stores it in S3, then invokes a second Lambda to download and evaluate the model.

The model will be first trained by the `ml-train` Lambda function and then uploaded on the S3 bucket.
A second Lambda function will download the model and run predictions on a test set of character inputs.
The logs of the Lambda invocation should be visible in the LocalStack container output (with `DEBUG=1` enabled):

```
>START RequestId: 65dc894d-25e0-168e-dea1-a3e8bfdb563b Version: $LATEST
> --> prediction result: [8 8 4 9 0 8 9 8 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 9 6 7 8 9
...
>  9 5 4 8 8 4 9 0 8 9 8]
> END RequestId: 65dc894d-25e0-168e-dea1-a3e8bfdb563b
```

## License

This code is available under the Apache 2.0 license.
