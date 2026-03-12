# Multi-Account Multi-Region S3 Access

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | S3, IAM                             |
| Integrations | AWS CLI                             |
| Categories   | Security; Multi-Account             |

## Introduction

A demo application illustrating how to access S3 resources across different AWS accounts using bucket policies and IAM users with LocalStack. The script uses the following AWS profiles to simulate a cross-account scenario:

- **Admin user of account A** with account ID `000000000001`
- **Admin user of account B** with account ID `000000000002`
- **Account A user** — creates the S3 bucket and grants cross-account access via bucket policies
- **Account B user** — copies resources from Account A's `source` bucket into its own `target` bucket

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
