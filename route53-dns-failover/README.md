# Route53 DNS Failover

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Route53, EC2                        |
| Integrations | Docker Compose, AWS CLI             |
| Categories   | Networking; DNS                     |

## Introduction

A demo application illustrating Route53 DNS failover based on health checks using LocalStack. The sample configures Route53 health checks and DNS records with failover routing policies, then demonstrates automatic DNS failover when the primary endpoint becomes unhealthy.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

This starts LocalStack and supporting services via Docker Compose.

## Run the application

```bash
make run
```

The script configures Route53 health checks and DNS failover routing, then demonstrates failover behavior.

## License

This code is available under the Apache 2.0 license.
