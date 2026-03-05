# Serverless Lambda Layers

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda                              |
| Integrations | Serverless Framework                |
| Categories   | Serverless                          |

## Introduction

A demo application illustrating Lambda layers using LocalStack, deployed via the Serverless framework. Lambda layers allow you to package shared code and dependencies separately from your function code, enabling reuse across multiple functions.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [Node.js](https://nodejs.org/en/download/) with `npm`
- [Serverless Framework](https://www.serverless.com/framework/docs/getting-started)

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

The script deploys the Lambda function with its layer via the Serverless framework and invokes it to verify the layer is loaded correctly.

## License

This code is available under the Apache 2.0 license.
