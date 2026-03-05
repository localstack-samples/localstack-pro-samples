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

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack. Set it with:
  ```bash
  export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
  ```
  You can find your token on the [LocalStack Web Application](https://app.localstack.cloud/workspace/auth-token).
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

```bash
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

## License

This code is available under the Apache 2.0 license.
