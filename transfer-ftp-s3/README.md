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
- [`lstk` CLI](https://docs.localstack.cloud/aws/developer-tools/running-localstack/lstk/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), used through `lstk aws`

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

You should then see log messages similar to:

```
Running Test: Creating FTP server and uploading files to S3 via Transfer API
Creating FTP server in AWS Transfer API
Connecting to AWS Transfer FTP server on local port 4510
Uploading file to FTP root directory
Uploading file to FTP sub-directory
Downloading files from S3 root and sub-directory
Test done.
```

## License

This code is available under the Apache 2.0 license.
