# Lambda Function URLs with Python

| Key          | Value                         |
| ------------ | ----------------------------- |
| Services     | Lambda                        |
| Integrations | AWS CLI, Terraform            |
| Categories   | Serverless; REST API          |

## Introduction

A demo application illustrating how to create a Python Lambda function with a function URL using LocalStack. Lambda function URLs provide a dedicated HTTP(S) endpoint for invoking a Lambda function directly without an API Gateway.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Python 3](https://www.python.org/downloads/)

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

The script:

- Packages the Lambda function with its dependencies.
- Creates the Lambda function in LocalStack.
- Configures a function URL with no authentication.

## License

This code is available under the Apache 2.0 license.
