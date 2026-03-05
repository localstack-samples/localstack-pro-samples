# Chalice REST API

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, API Gateway                 |
| Integrations | Chalice                             |
| Categories   | REST API; Serverless                |

## Introduction

A demo application illustrating the [AWS Chalice](https://github.com/aws/chalice) framework integration with LocalStack. The [`chalice-local`](https://github.com/localstack/chalice-local) client deploys and serves the REST API locally, enabling full local development and testing without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`chalice-local`](https://github.com/localstack/chalice-local) — install with `pip install chalice-local`
- [Python 3](https://www.python.org/downloads/)

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

The local development server starts and serves the API at `http://127.0.0.1:8000`.

## License

This code is available under the Apache 2.0 license.
