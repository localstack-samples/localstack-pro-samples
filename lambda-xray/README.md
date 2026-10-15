# Lambda X-Ray Tracing

| Key          | Value                                         |
| ------------ | --------------------------------------------- |
| Services     | Lambda, X-Ray, CloudFormation                 |
| Integrations | AWS CLI, AWS SAM                              |
| Categories   | Serverless; Observability                     |

## Introduction

A collection of samples demonstrating AWS X-Ray distributed tracing for Lambda functions using LocalStack. The samples show how to instrument Python Lambda functions with the AWS X-Ray SDK and AWS Powertools Tracer, and how to retrieve and inspect trace data locally.

## Sub-samples

| Sample                    | Description                                              |
| ------------------------- | -------------------------------------------------------- |
| [python-xray-sdk](python-xray-sdk)       | Lambda X-Ray tracing using the AWS X-Ray SDK for Python  |
| [python-powertools](python-powertools)   | Lambda X-Ray tracing using AWS Powertools Tracer         |

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`lstk` CLI](https://docs.localstack.cloud/aws/developer-tools/running-localstack/lstk/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), used through `lstk aws`
- [Python 3](https://www.python.org/downloads/) with `pip`

## Start LocalStack

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
lstk start
```

Refer to the individual sub-sample READMEs for deployment and invocation instructions.

## License

This code is available under the Apache 2.0 license.
