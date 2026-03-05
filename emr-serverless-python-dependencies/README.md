# EMR Serverless with Python Dependencies

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | EMR Serverless, S3, IAM             |
| Integrations | Terraform, AWS CLI                  |
| Categories   | Analytics; Big Data; Spark          |

## Introduction

A demo application illustrating how to add Python dependencies to an EMR Serverless Spark job using LocalStack. This sample implements a workaround for mounting Python environments directly into the LocalStack container, enabling PySpark jobs with custom dependencies to run locally.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) ~> 1.9.1

## Check prerequisites

```bash
make check
```

## Installation

```bash
make init
make build
```

## Start LocalStack

```bash
make start
```

## Deploy the Application

```bash
make deploy
```

The script creates IAM roles, an S3 bucket, and an EMR Serverless application via Terraform.

## Run the application

```bash
make run
```

## License

This code is available under the Apache 2.0 license.
