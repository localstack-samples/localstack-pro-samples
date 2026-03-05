# Glue Crawler with Redshift

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Glue, Redshift                      |
| Integrations | AWS CLI                             |
| Categories   | ETL; Analytics                      |

## Introduction

A demo application illustrating how to use AWS Glue Crawler to populate the Glue metadata store with the table schema of Redshift database tables using LocalStack. The sample demonstrates the full workflow from creating a Redshift cluster to running a crawler that discovers table metadata.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script:

- Creates a Redshift cluster and database.
- Creates a Glue connection with JDBC properties for the Redshift database.
- Creates a Glue database and a crawler.
- Runs the crawler to populate the Glue metadata store with Redshift table schemas.

## License

This code is available under the Apache 2.0 license.
