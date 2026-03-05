# Lambda Hot Reloading

| Key          | Value                         |
| ------------ | ----------------------------- |
| Services     | Lambda                        |
| Integrations | AWS CLI, Terraform            |
| Categories   | Serverless; Developer Experience |

## Introduction

A collection of samples demonstrating LocalStack's Lambda hot reloading capability, which enables immediate reflection of code changes without redeployment. Hot reloading significantly accelerates development cycles by watching local file changes and automatically updating Lambda function code.

## Sub-samples

| Sample                    | Description                                       |
| ------------------------- | ------------------------------------------------- |
| [javascript](javascript)  | Hot reloading with a JavaScript Lambda function   |
| [typescript](typescript)  | Hot reloading with a TypeScript Lambda function   |
| [javascript-terraform](javascript-terraform) | Hot reloading deployed via Terraform |
| [javascript-terraform-layers](javascript-terraform-layers) | Hot reloading with Lambda layers via Terraform |
| [lambda-typescript-webpack](lambda-typescript-webpack) | TypeScript Lambda with Webpack bundling |

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Node.js](https://nodejs.org/en/download/) with `npm`

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

## Run the application

```bash
make run
```

Refer to the individual sub-sample READMEs for more details on each variant.

## License

This code is available under the Apache 2.0 license.
