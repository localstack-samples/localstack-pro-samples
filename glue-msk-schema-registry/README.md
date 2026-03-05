# Glue Schema Registry with MSK

| Key          | Value                                                    |
| ------------ | -------------------------------------------------------- |
| Services     | MSK, Glue Schema Registry, Glue ETL, RDS                |
| Integrations | AWS CLI, Maven                                           |
| Categories   | Streaming; Analytics; Schema Evolution                   |

## Introduction

A demo application illustrating schema evolution with AWS Glue Schema Registry and AWS Managed Streaming for Kafka (MSK) using LocalStack. The sample demonstrates Kafka producers registering and validating Avro schemas, Kafka consumers reading schema-encoded records, and the full schema evolution lifecycle with compatibility enforcement.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Java 11](https://openjdk.org/) and [Maven 3](https://maven.apache.org/)

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

The script creates an MSK Kafka cluster and Glue Schema Registry, runs Kafka producers and consumers with Avro schemas, and demonstrates schema evolution with compatibility checking.

## License

This code is available under the Apache 2.0 license.
