# CDK Resources

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, SQS, SNS, AppSync           |
| Integrations | AWS CDK                             |
| Categories   | IaC; Serverless                     |

## Introduction

A demo application illustrating deployment of AWS resources locally using [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) with LocalStack. The [`cdklocal`](https://github.com/localstack/aws-cdk-local) wrapper is used to redirect CDK deployments to the local LocalStack endpoint.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`cdklocal`](https://github.com/localstack/aws-cdk-local) — install with `npm install -g aws-cdk-local`
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

The script bootstraps and deploys the CDK app to LocalStack using `cdklocal`.

## License

This code is available under the Apache 2.0 license.
