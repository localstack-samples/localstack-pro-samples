# Cognito Auth with JWT

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Cognito                             |
| Integrations | AWS CLI                             |
| Categories   | Authentication; Serverless          |

## Introduction

A demo application illustrating Cognito authentication and user pools running locally using LocalStack. The sample creates a Cognito user pool, registers a user, handles email verification, and demonstrates JWT-based authentication — all without connecting to AWS.

To receive Cognito email verification codes locally, configure the following environment variables before starting LocalStack:

- `SMTP_HOST`: hostname and port of your SMTP server (e.g., `host.docker.internal:2525`)
- `SMTP_USER`: SMTP username (optional)
- `SMTP_PASS`: SMTP password (optional)
- `SMTP_EMAIL`: email address used to send messages

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

The script runs an interactive Cognito authentication scenario. Make sure to configure the environment variable `$USER_EMAIL` with an email address before running.

At certain points, the script will prompt you to enter a confirmation code that has been sent to your email address (the code is also printed in the LocalStack logs):

```
Please check email inbox for ..., and enter the confirmation code below:
```

The script will then also ask you to specify a password reset code that is sent to your email:

```
Please check email inbox for ..., and enter the password reset code here:
```

> Credits: Kudos to `@Jaystified`, [Kurusugawa Computer Inc.](https://kurusugawa.jp) who kindly provided the initial version of the testing script in `test.sh`.

## License

This code is available under the Apache 2.0 license.
