# Glue ETL Jobs

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Glue, S3, RDS                       |
| Integrations | AWS CLI                             |
| Categories   | ETL; Analytics                      |

## Introduction

A demo application illustrating the use of the AWS Glue API to run local ETL (Extract, Transform, Load) jobs using LocalStack. The sample uploads a PySpark job script to S3, creates Glue databases and tables, and runs a Glue job to process data.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack. Set it with:
  ```bash
  export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
  ```
  You can find your token on the [LocalStack Web Application](https://app.localstack.cloud/workspace/auth-token).
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
make start
```

## Run the application

```bash
make run
```

The script uploads the PySpark job to S3, creates Glue databases and tables, starts the Glue job, and waits for it to complete.

## License

This code is available under the Apache 2.0 license.
