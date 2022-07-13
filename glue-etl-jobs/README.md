# LocalStack Demo: Data Processing with Glue ETL Jobs

Simple demo application illustrating the use of the Glue API to run local ETL jobs using LocalStack.

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

Please refer to the `job.py` PySpark job file and the `run.sh` script that runs the sample app.

## Running

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command prepares, creates, and runs the Glue job:

```
make run
```

After the run script completes, the logs in your terminal should look similar to the output below:
```
$ make run
Putting PySpark script to test S3 bucket ...
make_bucket: glue-pyspark-test
upload: ./job.py to s3://glue-pyspark-test/job.py               
Using local RDS database on port 4511 ...
Creating Glue databases and tables ...
Starting Glue job from PySpark script ...
{
    "Name": "test-job1"
}
Waiting for Glue job ID 'e4567287' to finish (current status: RUNNING) ...
Waiting for Glue job ID 'e4567287' to finish (current status: RUNNING) ...
Done - Glue job execution finished. Please check the LocalStack container logs for more details.
```

## License

This sample code is available under the Apache 2.0 license.
