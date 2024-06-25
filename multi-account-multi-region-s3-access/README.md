# Localstack Demo: Access S3 resources from different account and different region

Simple demo script to showcase the accessing of S3 resources from a different AWS account using bucket policies and IAM users with specific IAM policies attached to their identities.
The script uses a couple of AWS profiles to achieve that:

* Admin user of account A with account ID `000000000001`.

* Admin user of account B with account ID `000000000002`.

* Account A user that creates the S3 bucket and subsequent resources inside the bucket.

* Account B user that copies the resources from account A user's S3 bucket `source` into a bucket `target` it owns.

## Prerequisites

* LocalStack
* Docker
* Python 3.6+ / Python Pip
* `make`

## Installing

To install the dependencies:

```shell
make install
```

## Starting LocalStack

Make sure that LocalStack is started:

```shell
LOCALSTACK_AUTH_TOKEN=... make start
```

## Running

Run the sample demo script:

```shell
make run
```

## License

This code is available under the Apache 2.0 license.

