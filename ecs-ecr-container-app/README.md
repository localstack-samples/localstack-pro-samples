# ECS Container Application

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | ECS, ECR                            |
| Integrations | AWS CLI, CloudFormation, Docker     |
| Categories   | Containers; Serverless              |

## Introduction

A demo application illustrating ECS container applications running locally using LocalStack. The application image is built using Docker, pushed to a local ECR registry, and deployed via CloudFormation to an ECS cluster.

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

## Deploy the Application

```bash
make deploy
```

The script:

- Creates a new ECR registry locally.
- Builds the application Docker image from the `nginx` base image.
- Pushes the image to the ECR registry.
- Creates an ECS cluster and supporting infrastructure via CloudFormation.
- Deploys and starts the ECS application container in your local Docker environment.

Please refer to the `templates/` folder for details about the CloudFormation templates for the ECS service.

You should see a success output in the terminal:

```bash
...
Sample app (nginx) successfully deployed.
```

The nginx test app is accessible at `http://localhost:45139/` after deployment.

## License

This code is available under the Apache 2.0 license.
