# EMR Serverless Spark Jobs with Java

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | EMR Serverless, S3                  |
| Integrations | AWS CLI, Maven                      |
| Categories   | Analytics; Big Data; Spark          |

## Introduction

A demo application illustrating how to run a Java Spark job on EMR Serverless using LocalStack. The sample builds a Maven project, uploads the JAR to S3, creates an EMR Serverless application, and submits a Spark job — all locally without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
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

The script creates an S3 bucket and uploads the JAR file.

## Run the application

```bash
make run
```

The script creates an EMR Serverless Spark application, starts it, and submits a job that runs the `HelloWorld` class.

## License

This code is available under the Apache 2.0 license.
