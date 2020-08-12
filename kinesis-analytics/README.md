# LocalStack Demo: Continuous SQL Queries using Kinesis Data Analytics

Simple demo application using Kinesis Data Analytics to run continuous SQL queries over Kinesis data streams in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=cloudformation,kinesisanalytics,kinesis localstack start
```

Deploy the app locally and run a Lambda test invocation:
```
make run
```

The application first creates a Kinesis Data Analytics application, defined as a CloudFormation template. The core part of the application is the following SQL query, which continuously queries events from a Kinesis stream (input stream `input1_001`) and puts the reults on an output stream:
```
CREATE OR REPLACE STREAM input1_001 (
    symbol VARCHAR(20), price float, volume LONG)
DESCRIPTION 'Test description 123';
SELECT STREAM * FROM input1_001 WHERE volume < 150;
```

Once the application is deployed, the script adds a record to the input Kinesis stream and starts listening on the output Kinesis stream.

You should see a sequence of successful API calls in the output, similar to the logs below:
```
Deploying app to local environment
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/test-kinesis/155aca74-241b-45f9-aaf9-46d54302edd3"
}
Kinesis Analytics stack successfully deployed.
Sleeping some time to wait for the application and Kinesis listeners to start up ...
Application status: STARTING
Application status: STARTING
Application status: STARTING
Application status: STARTING
Application status: RUNNING
{
    "StreamNames": [
        "test-kinesis-InputKinesisStream-EGFMSL5IVBWR",
        "test-kinesis-OutputKinesisStream-8T65JCXG5C80"
    ]
}
{
    "ApplicationSummaries": [
        {
            "ApplicationName": "sampleApp",
            "ApplicationARN": "arn:aws:kinesisanalytics:us-east-1:000000000000:application/sampleApp",
            "ApplicationStatus": "RUNNING"
        }
    ]
}
Subscribing to output Kinesis stream test-kinesis-OutputKinesisStream-8T65JCXG5C80
Putting records to input Kinesis stream test-kinesis-InputKinesisStream-EGFMSL5IVBWR
{
    "ShardId": "shardId-000000000000",
    "SequenceNumber": "49609773071431768030359175072269323547206737796674879490"
}
Waiting for query results... (should print a record array with base64-encoded 'Data' below)
[
  {
    "SequenceNumber": "49609773071788579953535665042533895039569111718209519618",
    "ApproximateArrivalTimestamp": 1597244199.188,
    "Data": "WyJURVNUIiwgMTIzLCAxMDBd",
    "PartitionKey": "TEST"
  }
]
```

## License

This code is available under the Apache 2.0 license.
