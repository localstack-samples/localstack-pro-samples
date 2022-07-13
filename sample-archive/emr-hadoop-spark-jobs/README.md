# LocalStack Demo: Data Analytics via Elastic MapReduce

Simple demo application that illustrates running data analytics jobs using EMR APIs in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* `javac`

## Installing

To install the dependencies:
```
make install
```

## Project Details

This sample project creates a local EMR cluster and runs two simple jobs upon initialization:
1. A simple Java application (executed via `yarn`) that copies a file from one local S3 bucket to another
2. A simple Spark job that computes an approximation of Pi, and then creates a local S3 object to mark completion of the job

## Running

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=cloudformation,emr localstack start
```

Run the startup script:

```
make run
```

This script will run the following actions:
1. creates the EMR cluster locally,
2. compiles the Java code and builds the JAR file,
3. creates an EMR cluster and runs the two sample job as a startup steps

You should see a couple of outputs in the terminal, including:
```
Creating EMR cluster...
...
Waiting for job to complete running...
sleep 5
...
```

Finally, you should see some log lines indicating that the 2 jobs have run successfully:
```
The job should have copied file job1.xml to bucket bucket2:
awslocal s3 ls s3://bucket2/
2019-12-16 20:45:59          9 job1.xml
The Spark job should have copied file job2.xml to bucket bucket3:
awslocal s3 ls s3://bucket3/
2019-12-16 20:46:12          9 job2.xml
```

## License

This code is available under the Apache 2.0 license.
