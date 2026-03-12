# IAM Policy Enforcement

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | IAM, S3, Kinesis                    |
| Integrations | AWS CLI                             |
| Categories   | Security                            |

## Introduction

A demo application illustrating enforcement of IAM policies when working with local cloud APIs in LocalStack. The sample creates IAM users with specific policies and demonstrates allowed and denied API calls based on the configured permissions.

> Note: IAM enforcement is not enabled by default. Set `ENFORCE_IAM=1` before starting LocalStack to enable it.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Start LocalStack

The Makefile exports `ENFORCE_IAM=1` automatically. Start LocalStack with:

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script demonstrates:

- Denied Kinesis and S3 operations for users without the required IAM policies.
- Creating an IAM user with a policy that allows Kinesis access.
- Allowed Kinesis and S3 operations using the IAM credentials with the correct policy.

You should see output similar to:

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
