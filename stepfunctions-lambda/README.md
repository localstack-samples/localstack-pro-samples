# Step Functions with Lambda

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Step Functions, Lambda              |
| Integrations | AWS CLI                             |
| Categories   | Serverless; Orchestration           |

## Introduction

A demo application illustrating how to orchestrate Lambda functions using AWS Step Functions with LocalStack. The sample creates multiple Lambda functions and a Step Functions state machine that coordinates their execution.

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

## Deploy the Application

```bash
make deploy
```

## Run the application

```bash
make run
```

The script creates Lambda functions and a Step Functions state machine, then starts an execution that flows through the Lambda orchestration.

## License

This code is available under the Apache 2.0 license.
