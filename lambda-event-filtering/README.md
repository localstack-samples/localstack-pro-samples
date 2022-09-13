# AWS Lambda event filtering with DynamoDB and SQS

Simple demo application illustrating AWS Lambda event source filtering with DynamoDB and SQS. For this demo, we will use AWS Serverless Application Model (SAM), and a thin LocalStack wrapper `samlocal` to create our infrastructure through SAM on LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)
* [`samlocal`](https://github.com/localstack/aws-sam-cli-local)

## Installing

Setup [Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) and [AWS SAM CLI Local](https://github.com/localstack/aws-sam-cli-local) on your local machine. Start LocalStack via:

```sh 
localstack start -d
```

## Deploy the application

To setup the infrastructure on LocalStack, run:

```sh
samlocal deploy -g
```

You will be prompted to enter a name for the stack. Use the default options for the prompts and fill `Y` (`Yes`) for the confirmation prompt. The stack will be created and the output will be printed to the console.

If you have made any changes to the application, you can update the stack by running:

```sh
samlocal deploy 
```

After deploying you can send a SQS message to the queue and see the Lambda function being triggered:

```sh
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/MyQueue --message-body "{ "data" : "A" }" --delay-seconds 10
```

You will see a JSON output similar to the following:

```json
{
    "MD5OfMessageBody": "64dfee8647a8264b25b01b7f22d72d3a",
    "MessageId": "22fbddd2-5add-4a03-a850-152780d786c1"
}
```

## Destroy the application

To destroy the infrastructure on LocalStack, run:

```sh
samlocal delete
```
