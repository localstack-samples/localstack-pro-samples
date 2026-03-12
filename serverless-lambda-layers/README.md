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

You should see a success output:

```
{
    "StatusCode": 200
}
```

Check the LocalStack container logs for the Lambda output:

```
>START RequestId: ba4efc87-7bf9-1705-9f45-8e84ba8eb071 Version: $LATEST
> 2019-10-23T14:25:12.709Z	ba4efc87-7bf9-1705-9f45-8e84ba8eb071	INFO	This text should be printed in the Lambda
> END RequestId: ba4efc87-7bf9-1705-9f45-8e84ba8eb071
> REPORT RequestId: ba4efc87-7bf9-1705-9f45-8e84ba8eb071	Duration: 22.65 ms	Billed Duration: 100 ms	Memory Size: 1536 MB	Max Memory Used: 42 MB
```

## License

This code is available under the Apache 2.0 license.
