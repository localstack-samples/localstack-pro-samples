# EMR Serverless Sample

| Key          | Value                   |
| ------------ | ----------------------- |
| Services     | EMR Serverless, S3      |
| Integrations | AWS CLI, Maven          |
| Categories   | Analytics; Big Data     |

## Introduction

A demo application illustrating how to run a Java Spark job on EMR Serverless using LocalStack. The sample builds a Maven project, uploads the JAR to S3, and submits an EMR Serverless job.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`lstk` CLI](https://docs.localstack.cloud/aws/developer-tools/running-localstack/lstk/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), used through `lstk aws`
- [Java](https://openjdk.org/) and [Maven](https://maven.apache.org/)

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

## Deploy the Application

```bash
make deploy
```

The script creates an S3 bucket and uploads the compiled JAR file.

## Run the application

```bash
make run
```

The script creates an EMR Serverless application, starts it, and submits a Spark job.

## License

This code is available under the Apache 2.0 license.
