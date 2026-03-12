# Lambda Container Images

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, ECR                         |
| Integrations | AWS CLI, Docker                     |
| Categories   | Serverless; Containers              |

## Introduction

A demo application illustrating Lambda container images with LocalStack. The Lambda image is built using Docker and pushed to a local ECR registry, then deployed and invoked as a container-based Lambda function.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)

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

## Run the application

```bash
make run
```

The script:

- Creates a local ECR repository.
- Builds the Lambda Docker image and pushes it to the ECR registry.
- Deploys the Lambda function using the container image.
- Invokes the Lambda function and shows the response.

You should see output similar to:

```bash
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

The Lambda invocation logs are visible in the LocalStack container output (with `DEBUG=1` enabled):

```bash
DEBUG:localstack_ext.services.awslambda.lambda_extended: Log output for invocation of Lambda "ls-lambda-image":
INIT: Using Lambda API Runtime target host: 'ls-lambda-image.us-east-1.localhost.localstack.cloud:4566'
INIT: Starting daemons...
INIT: Host 'ls-lambda-image.us-east-1.localhost.localstack.cloud' resolves to '172.17.0.2'
-----
Hello from LocalStack Lambda container image!
```

## Troubleshooting

### UnsupportedMediaTypeException

```bash     
An error occurred (UnsupportedMediaTypeException) when calling the Invoke operation (reached max retries: 0): The payload is not JSON: b'\xb5\xeb-\xb5\xeb-'
```

**Solution**: Downgrade your `awslocal` CLI to version 1, or update the Lambda invocation to use `--cli-binary-format raw-in-base64-out`:

```bash
awslocal lambda invoke --cli-binary-format raw-in-base64-out \
    --function-name ls-lambda-image \
    --payload '{"test": "test"}' /tmp/lambda.out \
    --log-type Tail --query 'LogResult' --output text | base64 -d
```

## License

This code is available under the Apache 2.0 license.
