# LocalStack Demo: Hot code swapping for Lambda functions using LocalStack’s code mounting in JavaScript

## Prerequisites

* LocalStack
* Docker
* [awslocal](https://github.com/localstack/awscli-local) CLI
* Terraform
* [tflocal](https://github.com/localstack/terraform-local) CLI

## Introduction to the sample
Other than the deployment of the sample, it is practically identical to [our javascript hot reloading sample](../javascript/).

We will use terraform to deploy a hot reloaded lambda function, and then interact with it by invoking it and changing its source.

The source code of the created lambda function `hotreloadlambda` is located in the subfolder [lambda_src](./lambda_src/).


## Starting up

First, we need to make sure we start LocalStack with the right configuration. 
To use our new lambda provider, all you need to do is set `PROVIDER_OVERRIDE_LAMBDA=v2`, if you use a LocalStack version < 2.0.


If you want to use our old provider, please set `LAMBDA_REMOTE_DOCKER` to `0` (see the [Configuration Documentation](https://docs.localstack.cloud/localstack/configuration/#lambda) for more information):

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
      - LAMBDA_REMOTE_DOCKER=0
```

## Deploying

Now we can deploy our terraform stack by using `tflocal`.
First, we initialize the terraform working directory using:

```bash
tflocal init
```

We can now check the plan of terraform for our deployment:

```bash
tflocal plan
```

Afterwards, we can deploy our stack on LocalStack:

```bash
tflocal apply
```

The terraform configuration will automatically deploy the lambda with hot reloading for the function code.
The function code will be the contents of the `lambda_src` subdirectory.

## Invoking the Lambda function

We can quickly make sure that it works by invoking it with a simple payload:

```bash
awslocal lambda invoke --function-name hotreloadlambda output.txt
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

Now, that we got everything up and running, the fun begins. Because the function code directory, in our case `./lambda_src` is mounted into the executing container, any change that we save in this folder will affect the execution almost instantly.

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

