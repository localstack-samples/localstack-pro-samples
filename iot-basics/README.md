# IoT Basics

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | IoT                                 |
| Integrations | AWS CLI                             |
| Categories   | IoT                                 |

## Introduction

A demo application illustrating basic IoT API usage with LocalStack. The sample creates IoT things, policies, and certificates, then connects to the IoT MQTT endpoint to publish and subscribe to messages — all locally without connecting to AWS.

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

The script creates IoT things and policies, connects to the local MQTT endpoint, publishes messages, and verifies they are received by a subscriber.

## License

This code is available under the Apache 2.0 license.
