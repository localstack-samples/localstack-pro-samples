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

## License

This code is available under the Apache 2.0 license.
