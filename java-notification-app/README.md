# Java Notification App

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | CloudFormation, SNS, SQS, SES       |
| Integrations | AWS SDK, Docker Compose             |
| Categories   | Messaging; Notifications            |

## Introduction

A Spring Boot application demonstrating AWS messaging services with LocalStack. The sample provisions CloudFormation infrastructure for SNS/SQS subscriptions, processes messages from SQS using the AWS Java SDK, and sends email notifications via SES. A MailHog SMTP server runs alongside LocalStack for local email testing.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Java 11+](https://openjdk.org/) and [Maven 3+](https://maven.apache.org/)

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

This starts LocalStack and a MailHog SMTP server via Docker Compose. Access the MailHog UI at `http://localhost:8025/`.

## Deploy the Application

```bash
make deploy
```

Deploys the CloudFormation stack with SNS, SQS, and SES infrastructure.

## Run the application

```bash
make run
```

The script verifies the SES email identity, publishes an SNS message, processes the queued notification, and sends an email via SES.

## License

This code is available under the Apache 2.0 license.
