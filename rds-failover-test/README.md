# LocalStack Demo: RDS Failover Test

Simple demo application illustrating running a failover test against an RDS database.

## Prerequisites

* LocalStack
* Docker
* Python
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:

```bash
make install
```

## Starting LocalStack

Make sure that LocalStack is started:

```bash
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Run the scenario Python script `main.py` as follows:

```bash
make run
```

You should see some logs from the script, similar to the output below:

```bash
Creating global cluster 'global-cluster-1'
Creating primary DB cluster 'rds-cluster-1'
Creating secondary DB cluster 'rds-cluster-2'
Running assertions, to ensure the cluster writer has been updated
Start global DB cluster failover ...
✅ Test done - all assertions succeeded
```

## License

This code is available under the Apache 2.0 license.
