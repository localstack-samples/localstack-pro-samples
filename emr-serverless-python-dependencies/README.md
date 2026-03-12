# EMR Serverless with Python Dependencies

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | EMR Serverless, S3, IAM             |
| Integrations | Terraform, AWS CLI                  |
| Categories   | Analytics; Big Data; Spark          |

## Introduction

A demo application illustrating how to add Python dependencies to an EMR Serverless Spark job using LocalStack. This sample implements a workaround for mounting Python environments directly into the LocalStack container, enabling PySpark jobs with custom dependencies to run locally.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) ~> 1.9.1

## Check prerequisites

```bash
make check
```

## Installation

This initializes your Terraform workspaces:

```bash
make init
```

Build the Python dependencies for the Spark job. For LocalStack, we create a `/pyspark_env` folder that is mounted into the LocalStack container (rather than packaging it as a tarball like in AWS):

```bash
# For LocalStack: creates /pyspark_env folder
make build

# For AWS: creates pyspark_deps.tar.gz
make build-aws
```

## Start LocalStack

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Deploy the Application

Creates the following resources via Terraform: IAM role, IAM policy, S3 bucket, and an EMR Serverless application.

```bash
# Deploy to LocalStack (starts LocalStack via docker-compose and applies Terraform)
LOCALSTACK_AUTH_TOKEN=$LOCALSTACK_AUTH_TOKEN make deploy

# Deploy to AWS
make deploy-aws
```

## Run the application

We can finally run our Spark job. Notice the difference in `start_job.sh` between LocalStack and AWS: for AWS, `spark.archives` references `environment/bin/python`; for LocalStack, we rely on the volume-mounted container and use the absolute path `/tmp/environment/bin/python`.

```bash
# LocalStack
make run

# AWS
make run-aws
```

## Destroy the application

```bash
# LocalStack
make destroy

# AWS
make destroy-aws
```

## License

This code is available under the Apache 2.0 license.
