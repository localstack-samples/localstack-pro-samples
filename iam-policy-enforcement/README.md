# LocalStack Demo: IAM Policy Enforcement

Simple demo application illustrating enforcement of IAM policies when working with local cloud APIs in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`

## Installing

To install the dependencies:
```
make install
```

## Configuration

Please note that LocalStack by default does not enforce IAM policies. IAM needs to be manually enabled by setting the `ENFORCE_IAM=1` environment variable.

## Running

Make sure that the `ENFORCE_IAM=1` environment variable is enabled, and that LocalStack is started:
```
LOCALSTACK_API_KEY=... ENFORCE_IAM=1 DEBUG=1 localstack start
```

Run the script that is running the :
```
make run
```

You should see a couple of allowed and denied API calls (as per the IAM policies) in the terminal output:
```
Running IAM enforcement tests in local environment
Step 1: Trying to create Kinesis stream - should get DENIED ...
An error occurred (AccessDeniedException) when calling the CreateStream operation: Access to the specified resource is denied
Step 2: Trying to create S3 bucket - should get DENIED ...
make_bucket failed: s3://test-iam-bucket An error occurred (AccessDeniedException) when calling the CreateBucket operation: Access to the specified resource is denied
Step 3: Creating user with IAM policy to allow Kinesis access ...
        "UserName": "user1",

Done creating IAM users - now trying to create the same resources as above using the generated IAM credentials (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY) and associated policy

Step 4: Trying to create Kinesis stream using IAM credentials - should get ALLOWED ...
        "StreamStatus": "ACTIVE",
Step 5: Trying to create S3 bucket using IAM credentials - should get ALLOWED ...
make_bucket: test-iam-bucket
...
```

## License

This code is available under the Apache 2.0 license.
