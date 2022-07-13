# LocalStack Demo: RDS Database Queries

Simple demo application illustrating running queries against an RDS database.

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

You should see some logs from the script, similar to the output below:
```
Creating RDS DB instance
Run DB queries against RDS instance i1
[(1, 'Jane'), (2, 'Alex'), (3, 'Maria')]
Deleting RDS DB instance i1
```

## License

This code is available under the Apache 2.0 license.
