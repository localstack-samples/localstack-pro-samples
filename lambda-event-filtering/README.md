# Lambda Event Filtering with DynamoDB and SQS

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, DynamoDB, SQS               |
| Integrations | AWS SAM                             |
| Categories   | Serverless; Event-Driven            |

## Introduction

A demo application illustrating AWS Lambda event source filtering with DynamoDB and SQS using LocalStack. The sample uses AWS SAM and `samlocal` to deploy a Lambda function that is triggered only when SQS messages match specific filtering criteria defined on the DynamoDB stream.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [`samlocal`](https://github.com/localstack/aws-sam-cli-local) — install with `pip install aws-sam-cli-local`
- [Node.js](https://nodejs.org/en/download/) with `npm` and [`ulid`](https://www.npmjs.com/package/ulid) (`npm install --save ulid`)

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

To set up the infrastructure on LocalStack for the first time, use the guided deploy (prompts for a stack name and confirmation):

```bash
samlocal deploy -g
```

Use the default options for the prompts and enter `Y` for the confirmation. For subsequent deploys after making changes:

```bash
samlocal deploy
```

## Run the application

After deploying, send an SQS message to trigger the Lambda via the filter criteria:

```bash
awslocal sqs send-message \
    --queue-url http://localhost:4566/000000000000/MyQueue \
    --message-body '{"data": "A"}' \
    --delay-seconds 10
```

You will see a JSON output similar to the following:

```json
{
    "MD5OfMessageBody": "64dfee8647a8264b25b01b7f22d72d3a",
    "MessageId": "22fbddd2-5add-4a03-a850-152780d786c1"
}
```

In the `template.yaml` we have defined the DynamoDB table and the Stream function with a filtering criteria. We instruct the Stream function to trigger the Lambda function only when the filtering criteria is satisfied.

Using the SQS, we send a message body to the DynamoDB stream to match the specific filtering criteria. After the message is sent, we can see the Lambda function being triggered and you can check the logs to verify it.

## Destroy the application

```bash
samlocal delete
```

## License

This code is available under the Apache 2.0 license.
