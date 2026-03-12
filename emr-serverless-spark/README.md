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

## Configure a Custom AWS Profile (optional)

If not using `awslocal`, add the following profile to `~/.aws/config`:

```shell
[profile localstack]
region=us-east-1
output=json
endpoint_url = http://localhost:4566
```

And to `~/.aws/credentials`:

```shell
[localstack]
aws_access_key_id=test
aws_secret_access_key=test
```

## Installation

Build the Java Spark application (`java-demo-1.0.jar` is included; you can also rebuild it):

```bash
make install
```

## Start LocalStack

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Deploy the Application

Before creating the EMR Serverless job, we need to create a JAR file containing the Java code. We have the `java-demo-1.0.jar` file in the current directory. Alternatively, you can create the JAR file yourself by following the steps below.

```bash
cd hello-world
mvn package
```

Create an S3 bucket and upload the JAR file:

```bash
cd ..
make deploy
```

## Run the application

Creates an EMR Serverless Spark application (which will run Spark 3.3.0), starts it, and submits a job that runs the `HelloWorld` class:

```bash
make run
```

The Spark job submits with:
- Entry point: the JAR file in S3
- `--class HelloWorld`
- Spark logs written to `s3://<bucket>/logs/` (specified in the `logUri` parameter)

## Stop the application

To stop the EMR Serverless application after the job completes:

```bash
awslocal emr-serverless stop-application --application-id $APPLICATION_ID
```

## License

This code is available under the Apache 2.0 license.
