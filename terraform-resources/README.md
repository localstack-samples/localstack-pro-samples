# Terraform Resources

| Key          | Value                                                            |
| ------------ | ---------------------------------------------------------------- |
| Services     | S3, Lambda, API Gateway, RDS, ElastiCache, IAM                  |
| Integrations | Terraform                                                        |
| Categories   | IaC                                                              |

## Introduction

A demo application deploying various AWS resources to LocalStack via Terraform. The sample creates a range of AWS resources including S3 buckets, Lambda functions, API Gateway endpoints, RDS parameter groups, and ElastiCache clusters — all using `tflocal` to redirect Terraform to LocalStack.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)

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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Deploy the Application

```bash
make run
```

This initializes Terraform (if not already done) and runs `terraform apply --auto-approve`. You may need to confirm the creation by entering `yes`. You should see output similar to:

```
Plan: 10 to add, 0 to change, 0 to destroy.
aws_iam_role.invocation_role: Creating...
aws_api_gateway_rest_api.demo: Creating...
aws_iam_role.lambda: Creating...
aws_db_parameter_group.default: Creating...
aws_elasticache_cluster.my-redis: Creating...
aws_s3_bucket.test-bucket: Creating...
aws_api_gateway_rest_api.demo: Creation complete after 1s [id=iq0njx2s0a]
...
aws_elasticache_cluster.my-redis: Creation complete after 32s [id=my-redis-cluster]

Apply complete! Resources: 10 added, 0 changed, 0 destroyed.
```

## License

This code is available under the Apache 2.0 license.
