# EMR Serverless with Python dependencies

[AWS has this example](https://github.com/aws-samples/emr-serverless-samples/tree/main/examples/pyspark/dependencies) of how to add python dependencies to an emr job. Unfortunately, the same pattern isn't currently possible on LocalStack. This here will serve as a example of how to implement a workaround to still be able to add your own dependencies and module to your emr Spark jobs

## Requirements
- poetry
- Terraform ~>1.7.5
- Make
- [Terraform-local](https://github.com/localstack/terraform-local)
- [LocalStack](https://github.com/localstack/localstack)
- [awslocal](https://github.com/localstack/awscli-local)

## init

This will initialize your terraform and terraform workspaces

```
make init
```

## Build

This will build the python dependencies for the Spark job. This is where the first difference with AWS happens, as we will not package it like we do for aws, but intead will save the environment to our project folder to mount it to Localstack countainer.

```
# For LocalStack, we create a /pyspark_env folder
make build

# For aws, we create pyspark_deps.tar.gz
make build-aws
```

## Deploy

Creates the following resources
- iam role
- iam policy
- s3 bucket
- emr-serverless application

```
# Starts localstack using docker-compose, and apply the terraform configuration.
LOCALSTACK_AUTH_TOKEN=<your_auth_token> make deploy

# apply terraform configuration to AWS
make deploy-aws
```

## Run job

We can finally run our spark job. Notice the differences in the `start_job.sh` for LocalStack and aws. For aws we add `spark.archives` to our configuration and reference the path for the environment as `environment/bin/python`. Whereas for LocalStack, we rely on the volume mounted on our container instead of the archives and are using the absolute path for the environment `/tmp/environment/bin/python`.

```
# LocalStack
make run

# aws
make run-aws
```

## Destroy

Finally we can destroy the environment. We make sure to stop the application first.

```
# LocalStack
make destroy

# aws
make destroy-aws
```