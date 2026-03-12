# Glue ETL Jobs

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Glue, S3, RDS                       |
| Integrations | AWS CLI                             |
| Categories   | ETL; Analytics                      |

## Introduction

A demo application illustrating the use of the AWS Glue API to run local ETL (Extract, Transform, Load) jobs using LocalStack. The sample uploads a PySpark job script to S3, creates Glue databases and tables, and runs a Glue job to process data.

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

The script uploads the PySpark job to S3, creates Glue databases and tables, starts the Glue job, and waits for it to complete.

Please refer to the `job.py` PySpark job file and the `run.sh` script for implementation details.

You should see output similar to:

```
$ make run
Putting PySpark script to test S3 bucket ...
make_bucket: glue-pyspark-test
upload: ./job.py to s3://glue-pyspark-test/job.py
Using local RDS database on port 4511 ...
Creating Glue databases and tables ...
Starting Glue job from PySpark script ...
{
    "Name": "test-job1"
}
Waiting for Glue job ID 'e4567287' to finish (current status: RUNNING) ...
Waiting for Glue job ID 'e4567287' to finish (current status: RUNNING) ...
Done - Glue job execution finished. Please check the LocalStack container logs for more details.
```

## License

This code is available under the Apache 2.0 license.
