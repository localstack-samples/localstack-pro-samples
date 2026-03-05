# Terraform Resources

| Key          | Value                                                            |
| ------------ | ---------------------------------------------------------------- |
| Services     | S3, Lambda, API Gateway, RDS, ElastiCache, IAM                  |
| Integrations | Terraform                                                        |
| Categories   | IaC                                                              |

## Introduction

A demo application deploying various AWS resources to LocalStack via Terraform. The sample creates a range of AWS resources including S3 buckets, Lambda functions, API Gateway endpoints, RDS parameter groups, and ElastiCache clusters — all using `tflocal` to redirect Terraform to LocalStack.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)

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

The script initializes Terraform and applies the configuration to create all resources in LocalStack.

## License

This code is available under the Apache 2.0 license.
