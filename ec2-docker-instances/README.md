# EC2 Instances with Docker Backend

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | EC2, SSM                            |
| Integrations | AWS CLI                             |
| Categories   | Compute                             |

## Introduction

A demo application illustrating LocalStack EC2 and SSM functionality using the Docker backend. The sample creates Docker-backed EC2 instances, sends commands via SSM, captures output, takes snapshots as AMIs, and terminates instances.

> Note: This demo downloads the Ubuntu Docker image (~100MB) on first run.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [`jq`](https://stedolan.github.io/jq/)

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

The script:

- Creates a Docker-backed EC2 instance.
- Sends a command to the instance via SSM.
- Retrieves the standard output of the command.
- Snapshots the running instance into a new AMI.
- Terminates the instance.

## License

This code is available under the Apache 2.0 license.
