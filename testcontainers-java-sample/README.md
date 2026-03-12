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

## Run Example

- Import the project (e.g. in IntelliJ), 
- Configure your LOCALSTACK_AUTH_TOKEN as environment variable, 
- Run the test `TestRDS` in your IDE.

It will create a LocalStack Testcontainer and a PostgreSQL database instance using `RDSClient`.
The database will then be filled with some data, and queried afterwards.

## License

This code is available under the Apache 2.0 license.
