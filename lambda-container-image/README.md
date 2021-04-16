# LocalStack Demo: Lambda Container Images

Simple demo application illustrating Lambda container images in LocalStack. The Lambda image is built using Docker and pushed to a local ECR registry.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=lambda,ecr localstack start
```

The following command builds, deploys, and runs the Lambda container image locally:

```
make run
```

You should see some logs and a success output in the terminal:
```
$ make run
Creating a new ECR repository locally
Building the Docker image, pushing it to ECR URL: localhost:4513/repo1
...
Deploying Lambda function from container image locally
{
    "FunctionName": "ls-lambda-image",
    ...
    "PackageType": "Image"
}
Invoking Lambda function from container image
{
    "StatusCode": 200,
    "LogResult": "",
    "ExecutedVersion": "$LATEST"
}
Done - test successfully finished.
```

The logs of the Lambda invocation should be visible in the LocalStack container output (with `DEBUG=1` enabled):
```
DEBUG:localstack_ext.services.awslambda.lambda_extended: Log output for invocation of Lambda "ls-lambda-image":
INIT: Using Lambda API Runtime target host: 'ls-lambda-image.us-east-1.localhost.localstack.cloud:4566'
INIT: Starting daemons...
INIT: Host 'ls-lambda-image.us-east-1.localhost.localstack.cloud' resolves to '172.17.0.2'
Starting XRay server loop on UDP port 2000
Starting DNS server loop on UDP port 53
-----
Hello from LocalStack Lambda container image!
```

## License

This code is available under the Apache 2.0 license.
