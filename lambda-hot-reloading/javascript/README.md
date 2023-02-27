# LocalStack Demo: Hot code swapping for Lambda functions using LocalStack’s code mounting in JavaScript

## Prerequisites

* LocalStack
* Docker
* `awslocal` CLI

## Starting up

First, we need to make sure we start LocalStack with the right configuration. This is as simple as setting `LAMBDA_REMOTE_DOCKER`(see the [Configuration Documentation](https://docs.localstack.cloud/localstack/configuration/#lambda) for more information):

```bash
LAMBDA_REMOTE_DOCKER=0 localstack start
```

Accordingly, if you are launching LocalStack via Docker or Docker Compose:

```bash
#docker-compose.yml

services:
  localstack:
    ...
    environment:
      ...
      - LAMBDA_REMOTE_DOCKER=false
```

Now we need to create an IAM role, which is a collection of policies that grant specific permissions to access AWS resources on our mocked infrastructure. Before we create the role, we must define a trust policy for it. The trust policy has been defined in `trust-policy.json`. To create an IAM role, open your terminal in the directory where you want to create the role and run the following command:

```bash
awslocal iam create-role --role-name lambda-example --assume-role-policy-document ./trust-policy.json
```

To create the Lambda function, you now need to take care of only two things:

- Deploy via an S3 Bucket. You need to use the magic variable `hot-reload` as the bucket.
- Set the S3 key to the path of the directory your lambda function resides in. The handler is then referenced by the filename of your lambda code and the function in that code that needs to be invoked.

Push the following command to create the Lambda function:

```bash
awslocal lambda create-function --function-name myfirstlambda \
    --code S3Bucket="hot-reload",S3Key="/path/to/local/lambda/code" \
    --handler index.handler \
    --runtime nodejs14.x  \
    --role arn:aws:iam::000000000000:role/lambda-example
```

We can quickly make sure that it works by invoking it with a simple payload:

```bash
awslocal lambda invoke --function-name myfirstlambda output.txt
```

The invocation itself returns:

```json
{
	"Difference": 10,
	"Number1": 21,
	"Number2": 31,
	"Product": 651,
	"Quotient": 0.6774193548387096,
	"Sum": 52
}
```

## Changing things up

Now, that we got everything up and running, the fun begins. Because the function is now mounted as a file in the executing container, any change that we save on the file will be there in an instant.

For example, we can now make a minor change to the API and replace the `number1` and `number2` with new values, let's say 10 and 20. Without redeploying or updating the function, the result of the previous request will look like this:

```json
{
	"Difference": 10,
	"Number1": 10,
	"Number2": 20,
	"Product": 200,
	"Quotient": 0.5,
	"Sum": 30
}
```

