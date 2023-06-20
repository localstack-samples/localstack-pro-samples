# Creating a Lambda function with a function URL

In this example, we will demonstrate how to create an AWS Step Function with Lambda functions in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `awslocal` CLI

## Starting up

Start LocalStack via: 

```sh
localstack start -d
```

Run the following command to create the Lambda functions:

```sh
make create-lambdas
```

## Setting up and running Step Function

Create the Step Function:

```sh
awslocal stepfunctions create-state-machine --name step-demo \
  --definition "$(cat step-definition.json)" \
  --role-arn arn:aws:iam::000000000000:role/step-function-lambda
```

Start the execution:

```sh
awslocal stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:step-demo \
  --input '{"adam": "LocalStack", "cole": "Stack"}'
```

This creates and invokes the flow between the three Lambda functions we created using LocalStack earlier.
