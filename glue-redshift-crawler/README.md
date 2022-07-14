# LocalStack Demo: Glue Crawler RedShift Integration (JDBC)

Simple demo application illustrating the use of AWS Glue Crawler to populate the Glue 

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
This example shows how to use AWS Glue Crawler to populate the Glue metadata store with the table schema of RedShift database tables.

The following steps are executed when running the sample:
- Create a RedShift cluster and database.
- Create a Glue connection, specifying the JDBC connection properties for the RedShift database.
- Create a Glue database to store the table metadata in.
- Create a Crawler to populate the Glue database with the RedShift table metadata using the Glue connection.
- Create a new table in the RedShift database.
- Run the Crawler.
- Check out the resulting table metadata.

## Running
Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command executes the sample:

```
make run
```

## License

This sample code is available under the Apache 2.0 license.
