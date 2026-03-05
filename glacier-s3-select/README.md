# Glacier and S3 Select Queries

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | S3, Glacier                         |
| Integrations | AWS CLI                             |
| Categories   | Storage; Analytics                  |

## Introduction

A demo application illustrating the use of the Glacier API and S3 Select queries using LocalStack. The sample uploads CSV data, runs S3 Select queries to aggregate results, and demonstrates Glacier vault operations with select jobs.

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

The script:

- Creates S3 buckets, uploads CSV data, and runs S3 Select queries.
- Creates a Glacier vault and uploads a CSV file.
- Initiates a Glacier select job and downloads the query results.

## License

This code is available under the Apache 2.0 license.
