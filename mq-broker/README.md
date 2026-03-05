# MQ Broker

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | MQ                                  |
| Integrations | AWS CLI                             |
| Categories   | Messaging                           |

## Introduction

A demo application illustrating the use of the AWS MQ API with LocalStack. The sample creates a message broker, connects to it, sends a message to a queue, and cleans up the broker.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack. Set it with:
  ```bash
  export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
  ```
  You can find your token on the [LocalStack Web Application](https://app.localstack.cloud/workspace/auth-token).
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
make start
```

## Run the application

```bash
make run
```

The script creates an MQ broker, retrieves the broker endpoint, sends a message to the queue, and deletes the broker.

## License

This code is available under the Apache 2.0 license.
