# CDK for Terraform Resources

| Key          | Value                                  |
| ------------ | -------------------------------------- |
| Services     | SNS, DynamoDB, VPC                     |
| Integrations | CDK for Terraform, Terraform, Pipenv   |
| Categories   | IaC; Serverless                        |

## Introduction

A demo application illustrating deployment of AWS resources (SNS, DynamoDB, VPC) using [CDK for Terraform](https://developer.hashicorp.com/terraform/cdktf) with LocalStack. CDK for Terraform lets you define infrastructure using familiar programming languages and generates Terraform configuration from it.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)
- [`cdktf`](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install)
- [`pipenv`](https://pipenv.pypa.io/en/latest/)

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

## Deploy the Application

```bash
make deploy
```

The script:

- Synthesizes CDK for Terraform constructs into Terraform JSON configuration.
- Deploys an SNS topic, DynamoDB table, and VPC to LocalStack using Terraform.

## License

This code is available under the Apache 2.0 license.
