# Lambda Function URLs with JavaScript

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda                              |
| Integrations | AWS CLI, Terraform                  |
| Categories   | Serverless; REST API                |

## Introduction

A demo application illustrating how to create a JavaScript Lambda function with a function URL using LocalStack. Lambda function URLs provide a dedicated HTTP(S) endpoint for invoking a Lambda function directly. The sample also demonstrates deploying the same setup using Terraform.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) (optional, for Terraform-based deployment)

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

Deploy the Lambda function and create a function URL:

```bash
awslocal lambda create-function \
    --function-name localstack-lamba-url-example \
    --runtime nodejs20.x \
    --zip-file fileb://function.zip \
    --handler index.handler \
    --role arn:aws:iam::000000000000:role/cool-stacklifter

awslocal lambda create-function-url-config \
    --function-name localstack-lamba-url-example \
    --auth-type NONE
```

You will receive an HTTP URL in the form `http://abcdefgh.lambda-url.us-east-1.localhost.localstack.cloud:4566`. Invoke the Lambda function via HTTP POST:

```sh
curl -X POST \
    'http://abcdefgh.lambda-url.us-east-1.localhost.localstack.cloud:4566/' \
    -H 'Content-Type: application/json' \
    -d '{"num1": "10", "num2": "10"}'
```

Expected output:

```
The product of 10 and 10 is 100
```

## Using Terraform

You can automate the Lambda function and function URL creation using Terraform:

```sh
terraform init
terraform plan
terraform apply --auto-approve
```

Since we are using LocalStack, no actual AWS resources will be created. LocalStack creates ephemeral development resources that are automatically cleaned up when you stop LocalStack (`localstack stop`).

## License

This code is available under the Apache 2.0 license.
