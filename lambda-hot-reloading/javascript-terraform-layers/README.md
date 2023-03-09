# LocalStack Demo: Hot code swapping for Lambda functions using LocalStack’s code mounting in JavaScript

## Prerequisites

* LocalStack Pro
* Docker
* [awslocal](https://github.com/localstack/awscli-local) CLI
* Terraform
* [tflocal](https://github.com/localstack/terraform-local) CLI

## Introduction to the sample
In this sample, we demonstrate a hot reloading setup where both the function code and the layer code are hot reloaded.
Any changes to either of those two directories will reload the function. The changed code will be available almost immediately for the next invocation.

We will again re-use the sample from our [javascript](../javascript/) sample, but one of the values we want to change is supplied by a function defined in our layer.

We will use terraform to deploy a hot reloaded lambda function and invoke it once. Afterwards we will change its source and invoke it again to demonstrate the hot-reload feature.

The source code of the created lambda function `hotreloadlambda` is located in the subfolder [lambda_src](./lambda_src/) and the source code of the created layer `hot_reload_layer` is located in the subfolder [layer_src](./layer_src/).


## Starting up

First, we need to make sure we start LocalStack with the right configuration. 
Hot reloading of layers is only supported in our new lambda provider, all you need to do is set `PROVIDER_OVERRIDE_LAMBDA=v2`, if you use a LocalStack version < 2.0.

```bash
PROVIDER_OVERRIDE_LAMBDA=v2 localstack start
```

Accordingly, if you are launching LocalStack via Docker or Docker Compose:

```bash
#docker-compose.yml

services:
  localstack:
    ...
    environment:
      ...
      - PROVIDER_OVERRIDE_LAMBDA=v2
```

## Deploying

Now we can deploy our terraform stack by using `tflocal`.
First, we initialize the terraform working directory using:

```bash
tflocal init
```

Afterwards, we can deploy our stack on LocalStack:

```bash
tflocal apply
```

The terraform configuration will automatically deploy the lambda with hot reloading for the function code.
The function code consists of the contents of the `lambda_src` subdirectory and the layer code in the `layer_src` subdirectory.

## Invoking the Lambda function

We can quickly make sure that our deployed function works by invoking it with a simple payload:

```bash
awslocal lambda invoke --function-name hotreloadlambda output.txt
```

The invocation response:

```json
{
    "Number1": 21,
    "Number2": 31,
    "Sum": 52,
    "Product": 651,
    "Difference": 10,
    "Quotient": 0.6774193548387096
}
```

## Changing things up

Now, that we got everything up and running, the real fun begins. Because the function code directory, in our case `./lambda_src`, is mounted directly into the executing container, any changes that we make in this folder will be reflected in the execution almost instantly.

To demonstrate this behavior, we can now make a minor change to the API and replace `number2` with a new value, let's say 20. Without redeploying or updating the function, the result of the previous request will look like this:

```json
{
    "Number1": 21,
    "Number2": 20,
    "Sum": 41,
    "Product": 420,
    "Difference": 1,
    "Quotient": 1.05
}
```

We can now also change the value provided by our layer. Let's replace it with 10, by editing the index.js in our `./layer_src/nodejs/node_modules/test-dep` folder.

Our output after another invoke will be:

```json
{
    "Number1": 10,
    "Number2": 20,
    "Sum": 30,
    "Product": 200,
    "Difference": 10,
    "Quotient": 0.5
}
```

Now we can change layer and function independently or together, and test the outcome in real time.