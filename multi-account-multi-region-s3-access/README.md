# Multi-Account Multi-Region S3 Access

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | S3, IAM                             |
| Integrations | AWS CLI                             |
| Categories   | Security; Multi-Account             |

## Introduction

A demo application illustrating how to access S3 resources across different AWS accounts using bucket policies and IAM users with LocalStack. The sample uses two simulated accounts — Account A creates an S3 bucket and sets policies, while Account B accesses and copies resources from Account A's bucket into its own.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Python 3](https://www.python.org/downloads/) with `pip`

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

The script sets up two AWS accounts with IAM users and bucket policies, then demonstrates cross-account S3 resource access.

## License

This code is available under the Apache 2.0 license.
