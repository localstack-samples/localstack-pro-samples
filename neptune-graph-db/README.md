# Neptune Graph Database

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Neptune                             |
| Integrations | AWS CLI                             |
| Categories   | Graph Database                      |

## Introduction

A demo application illustrating Neptune Graph DB queries running locally using LocalStack. The sample creates a Neptune cluster, connects to it via Gremlin, and performs graph operations — adding vertices and querying the graph — all without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
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
make start
```

## Run the application

```bash
make run
```

The script creates a Neptune cluster, connects via Gremlin WebSocket, submits values, adds vertices to the graph, and queries the results.

## License

This code is available under the Apache 2.0 license.
