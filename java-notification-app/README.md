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

This will install the Maven dependencies for the project and build the project.

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

Start the Spring Boot application (requires dummy AWS credentials as environment variables):

```bash
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test mvn spring-boot:run
```

### Test the application

Run everything via `make run` or follow the steps below.

Verify the sender email address configured in the app:

```bash
awslocal ses verify-email-identity --email-address no-reply@localstack.cloud
```

Send a message to the topic:

```bash
awslocal sns publish --topic arn:aws:sns:us-east-1:000000000000:email-notifications --message '{"subject":"hello", "address": "alice@example.com", "body": "hello world"}'
```

Run the `/process` endpoint to send the queued notifications as emails:

```bash
curl -s localhost:8080/process
```

Verify that the email has been sent:

- either check MailHog via the UI http://localhost:8025/
- or query the LocalStack internal SES endpoint: `curl -s localhost:4566/_localstack/ses | jq .`

## License

This code is available under the Apache 2.0 license.
