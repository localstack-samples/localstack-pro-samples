# PHP/Bref Lambda with CDK

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, API Gateway                 |
| Integrations | AWS CDK, Bref, PHP                  |
| Categories   | Serverless; PHP                     |

## Introduction

A [PHP/Bref](https://bref.sh/) serverless application using a shared Lambda layer deployable with AWS CDK to LocalStack. The application implements a typed PHP Lambda handler as an HTTP handler class for serving API Gateway HTTP events. Bref turns API Gateway events into PSR-7 requests for PHP processing.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`cdklocal`](https://github.com/localstack/aws-cdk-local) — install with `npm install -g aws-cdk-local`
- [Node.js](https://nodejs.org/en/download/) with `npm`
- [`curl`](https://curl.se/) and [`jq`](https://stedolan.github.io/jq/)

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

The script bootstraps and deploys the CDK app locally, then invokes the HTTP endpoint via `curl`.

## License

This code is available under the Apache 2.0 license.
