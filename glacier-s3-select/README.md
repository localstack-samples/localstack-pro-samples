# LocalStack Demo: Gacier and S3 Select Queries

Simple demo application illustrating the use of Glacier API and S3 Select queries using LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## App Details

Please refer to the `test.csv` file and feel free to modify in order to see changes in the query results.

## Running

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command creates local S3 buckets and Glacier vaults, and runs simple demo queries over the `data.csv` CSV file:

```
make run
```

After the test script completes, the logs in your terminal should look similar to the output below:
```
$ make run
Creating S3 bucket and Glacier vault in LocalStack
make_bucket: test1
upload: ./data.csv to s3://test1/data.csv
Running S3 Select query against CSV file in bucket
Query results for S3 Select query below
----
count(*), sum(Cost)
10, 68.44
----
Creating new vault in local Glacier API
make_bucket: glacier-results
Uploading test CSV file to new Glacier vault
Initiating new "select" job in Glacier to query data from CSV file in vault archive
Sleep some time to wait for Glacier job to finish

Contents of result bucket after running Glacier query:
2020-04-19 23:51:50         29 78df3a1d

Downloading test CSV file from new Glacier vault
download: s3://glacier-results/test/query1/d47b7df7/results/78df3a1d to ./glacier-result.csv
Query results for S3 Select query below
----
count(*), sum(Cost)
10, 68.44
----
```

## License

This code is available under the Apache 2.0 license.
