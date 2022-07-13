# LocalStack Demo: Quantum Ledger Database (QLDB) Queries

Simple demo application illustrating running queries against a QLDB ledger on your local machine, using LocalStack.

## Prerequisites

* LocalStack
* Docker
* Python
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Run the scenario Python script `query.py` as follows:
```
make run
```

The test script creates a new QLDB ledger, and runs a couple of queries to INSERT and SELECT data from the ledger journal.

You should see some logs from the script, similar to the output below:
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
