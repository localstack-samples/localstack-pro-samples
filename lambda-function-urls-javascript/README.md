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
make start
```

## Run the application

```bash
make run
```

The script creates a Lambda function with a function URL and demonstrates invocation via HTTP POST.

## License

This code is available under the Apache 2.0 license.
