# QLDB Ledger Queries

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | QLDB                                |
| Integrations | AWS CLI                             |
| Categories   | Database                            |

## Introduction

A demo application illustrating running queries against a Quantum Ledger Database (QLDB) ledger locally using LocalStack. The sample creates a QLDB ledger, runs INSERT and SELECT queries, and demonstrates join operations between tables in the ledger journal.

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

The script creates a QLDB ledger, inserts test data, runs SELECT queries, and demonstrates join operations across tables.

You should see output similar to:

```
Scenario 1: create and list tables in ledger
-----------
Creating new test ledger in QLDB API: ledger-test-1
Creating two test tables in ledger
Retrieves list of tables in ledger ledger-test-1: ['foobar1', 'foobar2']
-----------
Scenario 2: create ledger tables and run join query
-----------
Creating two test tables in ledger - "Vehicle" and "VehicleRegistration"
Running a query that joins data from the two tables
Query result: [{'Vehicle': {'id': 'v1'}}, {'Vehicle': {'id': 'v2'}}, {'Vehicle': {'id': 'v3'}}]
```

## License

This code is available under the Apache 2.0 license.
