# Creating a Lambda function with a function URL

In this example, we will demonstrate how to create a Lambda function with a function URL. With the Function URL property, there is now a new way to call a Lambda Function via HTTP API call.

## Prerequisites

* LocalStack
* Docker
* `awslocal` CLI
* Terraform

## Starting up

Start LocalStack via: 

```sh
localstack start -d
```

Push the following command to deploy the Lambda function:

```sh
awslocal lambda create-function \
    --function-name localstack-lamba-url-example \
    --runtime nodejs14.x \
    --zip-file fileb://function.zip \
    --handler index.handler \
    --role cool-stacklifter
```

## Creating a Lambda function URL

With the Function URL property, there is now a new way to call a Lambda Function via HTTP API call using the `create-function-url-config` command.

```sh 
awslocal lambda create-function-url-config \
    --function-name localstack-lamba-url-example \
    --auth-type NONE
```

You will retrieve a HTTP URL that you can use to invoke the Lambda function, in the form of `http://abcdefgh.lambda-url.us-east-1.localhost.localstack.cloud:4566`.

You can now trigger the Lambda function by sending a HTTP POST request to the URL using `curl`:

```sh
curl -X POST \
    'http://abcdefgh.lambda-url.us-east-1.localhost.localstack.cloud:4566/' \
    -H 'Content-Type: application/json' \
    -d '{"num1": "10", "num2": "10"}'
```

The following output would be retrieved:

```sh 
The product of 10 and 10 is 100% 
```

## Using Terraform

You can use Terraform to automate the creation of Lambda function and to create a function URL. Run the following commands on your terminal to create the Lambda function and the function URL:

```sh
terraform init 
terraform plan
terraform apply --auto-approve
```

Since we are using LocalStack, no actual AWS resources will be created. Instead, LocalStack will create ephemeral development resources, which will automatically be cleaned once you stop LocalStack (using `localstack stop`).
