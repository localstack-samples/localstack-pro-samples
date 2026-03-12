# Athena Queries over S3 Files

| Key          | Value                          |
| ------------ | ------------------------------ |
| Services     | Athena, S3                     |
| Integrations | AWS CLI                        |
| Categories   | Analytics; Serverless          |

## Introduction

A demo application illustrating how to run Athena queries over S3 files locally using LocalStack. The sample uploads CSV test data to S3, creates Athena table metadata, and runs SQL queries to aggregate results — all without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Node.js](https://nodejs.org/en/download/) with `npm`

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

- Creates an S3 bucket and uploads CSV test data (person details) to the bucket.
- Runs queries to create Athena database and table metadata.
- Executes a SELECT query to count users by gender.
- Downloads and displays the query results from the S3 results bucket.

You should see output similar to:

```
$ ./run.sh
Uploading test data to S3...
make_bucket: athena-test
upload: data/data.csv to s3://athena-test/data/data.csv
Running queries to create database and table definitions...
NOTE: This can take a very long time (several minutes) as the system is initializing
Waiting for completion status of query cda0572a: RUNNING
...
Waiting for completion status of query cda0572a: SUCCEEDED
Starting SELECT query over data in S3. Query ID: 8a19e3a3
S3 query output location: s3://athena-test/results/Unsaved/2020/02/18/8a19e3a3
Waiting for query results to become available in S3 (this can take some time)
download: s3://athena-test/results/Unsaved/2020/02/18/8a19e3a3/results.csv to /tmp/8a19e3a3.results.csv
Query result downloaded from S3:
Male,49
Female,51
```

## License

This code is available under the Apache 2.0 license.
