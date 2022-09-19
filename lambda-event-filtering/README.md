# AWS Lambda event filtering with DynamoDB and SQS

Simple demo application illustrating AWS Lambda event source filtering with DynamoDB and SQS. For this demo, we will use AWS Serverless Application Model (SAM), and a thin LocalStack wrapper `samlocal` to create our infrastructure through SAM on LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)
* [`samlocal`](https://github.com/localstack/aws-sam-cli-local)
* NodeJS 14.x
* [`ulid`](https://www.npmjs.com/package/ulid)

## Installing

Setup [Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) and [AWS SAM CLI Local](https://github.com/localstack/aws-sam-cli-local) on your local machine. We also recommend using NodeJS 14.x alongside a [Node Version Manager](https://github.com/nvm-sh/nvm) to manage your NodeJS versions.


Start LocalStack via:

```sh 
localstack start -d
```

## Deploy the application

Let us first install the local dependencies:

```sh
npm install --save ulid
```

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

In the `template.yaml` we have defined the DynamoDB table and the Stream function with a filtering criteria. We instruct the Stream function to trigger the Lambda function only when the filtering criteria is satisfied.

Using the SQS, we send a message body to the DynamoDB stream to match the specific filtering criteria. After the message is sent, we can see the Lambda function being triggered and you can check the logs to verify it.

## Destroy the application

To destroy the infrastructure on LocalStack, run:

```sh
samlocal delete
```
