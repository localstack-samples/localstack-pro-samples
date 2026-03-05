# CloudWatch Metrics Alarm

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | CloudWatch, Lambda, SNS, SES        |
| Integrations | AWS CLI                             |
| Categories   | Monitoring; Serverless              |

## Introduction

A demo application illustrating how to create a CloudWatch metric alarm that triggers when a Lambda function fails using LocalStack. The alarm sends an SNS notification via email when the Lambda error count exceeds the threshold.

To receive email notifications locally, you need a mock SMTP server such as [smtp4dev](https://github.com/rnwood/smtp4dev) or [Papercut SMTP](https://github.com/ChangemakerStudios/Papercut-SMTP). Configure the following environment variables before starting LocalStack:

- `SMTP_HOST`: hostname and port of your mock SMTP server (e.g., `host.docker.internal:2525`)
- `SMTP_USER`: SMTP username (optional)
- `SMTP_PASS`: SMTP password (optional)

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [`jq`](https://stedolan.github.io/jq/)

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

The script:

- Creates a failing Lambda function.
- Creates an SNS topic and subscribes an email address.
- Creates a CloudWatch alarm based on Lambda error metrics.
- Invokes the Lambda function to trigger the alarm.
- Waits for the alarm state to change and confirms the notification.

## License

This code is available under the Apache 2.0 license.
