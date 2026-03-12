# ELB Application Load Balancers

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | ELB, Lambda                         |
| Integrations | Serverless Framework                |
| Categories   | Networking; Serverless              |

## Introduction

A demo application illustrating ELBv2 Application Load Balancers using LocalStack, deployed via the Serverless framework. The sample deploys Lambda functions behind an Application Load Balancer and demonstrates HTTP invocations through the ELB endpoints.

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

The script deploys the Serverless application and invokes the Lambda functions via ELB endpoints `/hello1` and `/hello2`.

You should see output similar to:

```bash
> sls deploy --stage local
...
Serverless app successfully deployed. Now trying to invoke the Lambda functions via ELB endpoint.
...
Invoking endpoint 1: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello1
"Hello 1"
Invoking endpoint 2: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello2
"Hello 2"
```

## License

This code is available under the Apache 2.0 license.
