# RDS with LocalStack Testcontainers

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | RDS                                 |
| Integrations | Testcontainers, Java                |
| Categories   | Database; Testing                   |

## Introduction

A demo application illustrating how to use LocalStack Testcontainers with RDS in Java. Testcontainers requires a special setup for RDS because the service may expose the database on any port. The sample demonstrates the port mapping configuration needed to connect to an RDS PostgreSQL instance from your test code.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [Java](https://openjdk.org/) and [Maven](https://maven.apache.org/)

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Run the application

```bash
make run
```

The Testcontainers library manages the LocalStack container lifecycle automatically. The test creates a LocalStack container, provisions an RDS PostgreSQL instance, inserts data, and queries it.

## License

This code is available under the Apache 2.0 license.
