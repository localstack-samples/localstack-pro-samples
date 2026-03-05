# FTP Upload to S3 via AWS Transfer API

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Transfer, S3                        |
| Integrations | AWS CLI                             |
| Categories   | File Transfer; Storage              |

## Introduction

A demo application illustrating the use of the AWS Transfer API with LocalStack. The sample creates a local FTP server via the Transfer API, uploads files via FTP, and downloads the uploaded files from the target S3 bucket.

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

The script creates an FTP server via the AWS Transfer API, uploads two files (to root and a sub-directory), then downloads and verifies them from the target S3 bucket.

## License

This code is available under the Apache 2.0 license.
