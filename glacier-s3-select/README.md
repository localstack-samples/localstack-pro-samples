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

Please refer to the `test.csv` file and feel free to modify it to see changes in the query results.

You should see output similar to:

```
$ make run
Creating S3 bucket and Glacier vault in LocalStack
make_bucket: test1
upload: ./data.csv to s3://test1/data.csv
Running S3 Select query against CSV file in bucket
Query results for S3 Select query below
----
count(*), sum(Cost)
10, 68.44
----
Creating new vault in local Glacier API
make_bucket: glacier-results
Uploading test CSV file to new Glacier vault
Initiating new "select" job in Glacier to query data from CSV file in vault archive
Sleep some time to wait for Glacier job to finish

Contents of result bucket after running Glacier query:
2020-04-19 23:51:50         29 78df3a1d

Downloading test CSV file from new Glacier vault
download: s3://glacier-results/test/query1/d47b7df7/results/78df3a1d to ./glacier-result.csv
Query results for S3 Select query below
----
count(*), sum(Cost)
10, 68.44
----
```

## License

This code is available under the Apache 2.0 license.
