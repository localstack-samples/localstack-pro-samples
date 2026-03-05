# Lambda Event Filtering with DynamoDB and SQS

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, DynamoDB, SQS               |
| Integrations | AWS SAM                             |
| Categories   | Serverless; Event-Driven            |

## Introduction

A demo application illustrating AWS Lambda event source filtering with DynamoDB and SQS using LocalStack. The sample uses AWS SAM and `samlocal` to deploy a Lambda function that is triggered only when SQS messages match specific filtering criteria defined on the DynamoDB stream.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack. Set it with:
  ```bash
  export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
  ```
  You can find your token on the [LocalStack Web Application](https://app.localstack.cloud/workspace/auth-token).
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [`samlocal`](https://github.com/localstack/aws-sam-cli-local) — install with `pip install aws-sam-cli-local`
- [Node.js](https://nodejs.org/en/download/) with `npm`

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

## Deploy the Application

```bash
make deploy
```

## Run the application

```bash
make run
```

The script sends an SQS message matching the filter criteria to trigger the Lambda function. Check the LocalStack logs to verify the function was invoked.

## License

This code is available under the Apache 2.0 license.
