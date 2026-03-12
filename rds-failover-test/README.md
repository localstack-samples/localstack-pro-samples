# RDS Failover Test

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | RDS                                 |
| Integrations | AWS CLI                             |
| Categories   | Database; Resilience                |

## Introduction

A demo application illustrating RDS global cluster failover testing with LocalStack. The sample creates a global RDS cluster with primary and secondary clusters, then triggers a failover to verify that the cluster writer is updated correctly.

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

The script creates a global RDS cluster with primary and secondary instances, triggers a failover, and verifies the cluster writer has been updated.

You should see output similar to:

```
Creating global cluster 'global-cluster-1'
Creating primary DB cluster 'rds-cluster-1'
Creating secondary DB cluster 'rds-cluster-2'
Running assertions, to ensure the cluster writer has been updated
Start global DB cluster failover ...
✅ Test done - all assertions succeeded
```

## License

This code is available under the Apache 2.0 license.
