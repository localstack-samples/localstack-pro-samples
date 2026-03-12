# RDS Database Queries

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | RDS                                 |
| Integrations | AWS CLI                             |
| Categories   | Database                            |

## Introduction

A demo application illustrating running queries against an RDS database locally using LocalStack. The sample creates an RDS DB instance, executes SQL INSERT and SELECT queries, and cleans up the instance.

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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script creates an RDS DB instance, runs queries to insert and retrieve records, and deletes the instance.

You should see output similar to:

```
Creating RDS DB instance
Run DB queries against RDS instance i1
[(1, 'Jane'), (2, 'Alex'), (3, 'Maria')]
Deleting RDS DB instance i1
```

## License

This code is available under the Apache 2.0 license.
