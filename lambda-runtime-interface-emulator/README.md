# Lambda Runtime Interface Emulator with LocalStack

In this example, we will locally test Lambda functions packaged as container images through Lambda Runtime Interface Emulator (RIE) in LocalStack. The Lambda function is implemented in Ruby, and we will use a Docker container image to install the [AWS Lambda Runtime interface emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator), which would be pushed to a local ECR registry, and then deployed as a Lambda function.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:

```sh
make install
```

## Running

Make sure that LocalStack is started:

```sh
PROVIDER_OVERRIDE_LAMBDA=asf LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command builds, deploys, and runs the Lambda container image locally:

```sh
make run
```

You should see some logs and a success output in the terminal:

```
$ make run
Creating a new ECR repository locally
...
Invoking Lambda function from container image
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
"Hello World!"
Done - test successfully finished.
```

## License

This code is available under the Apache 2.0 license.
