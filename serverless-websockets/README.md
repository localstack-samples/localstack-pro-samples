# Serverless WebSockets

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | API Gateway, Lambda                 |
| Integrations | Serverless Framework                |
| Categories   | Serverless; WebSockets              |

## Introduction

A demo application illustrating API Gateway V2 WebSocket APIs using LocalStack, deployed via the Serverless framework. The sample deploys a Lambda function connected to a WebSocket API and demonstrates bidirectional message passing over the WebSocket connection.

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

The script deploys the WebSocket API via Serverless, connects a WebSocket client, sends a test message, and verifies it is echoed back by the Lambda handler.

## License

This code is available under the Apache 2.0 license.
