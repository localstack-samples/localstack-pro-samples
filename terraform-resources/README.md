# LocalStack Demo: Create Local AWS Resources via Terraform

Simple demo project deploying various AWS resources to LocalStack via Terraform.

## Prerequisites

* LocalStack
* Docker
* Terraform
* `make`

## Installing

Install the dependencies using this command:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Create the resources via Terraform locally in LocalStack:
```
make start
```

You may need to confirm the creation by entering "yes". You should then see log output similar to the one below:
```
...
  Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

Plan: 10 to add, 0 to change, 0 to destroy.
aws_iam_role.invocation_role: Creating...
aws_api_gateway_rest_api.demo: Creating...
aws_iam_role.lambda: Creating...
aws_db_parameter_group.default: Creating...
aws_elasticache_cluster.my-redis: Creating...
aws_s3_bucket.test-bucket: Creating...
aws_api_gateway_rest_api.demo: Creation complete after 1s [id=iq0njx2s0a]
aws_iam_role.invocation_role: Creation complete after 1s [id=api_gateway_auth_invocation]
aws_iam_role.lambda: Creation complete after 1s [id=demo-lambda]
aws_iam_role_policy.invocation_policy: Creating...
aws_lambda_function.authorizer: Creating...
aws_iam_role_policy.invocation_policy: Creation complete after 0s [id=api_gateway_auth_invocation:default]
aws_s3_bucket.test-bucket: Creation complete after 2s [id=my-bucket]
aws_s3_bucket_acl.test-bucket-acl: Creating...
aws_s3_bucket_acl.test-bucket-acl: Creation complete after 0s [id=my-bucket,private]
aws_db_parameter_group.default: Creation complete after 2s [id=rds-pg]
aws_lambda_function.authorizer: Creation complete after 7s [id=api_gateway_authorizer]
aws_api_gateway_authorizer.demo: Creating...
aws_api_gateway_authorizer.demo: Creation complete after 0s [id=9a2570]
aws_elasticache_cluster.my-redis: Still creating... [10s elapsed]
aws_elasticache_cluster.my-redis: Still creating... [20s elapsed]
aws_elasticache_cluster.my-redis: Still creating... [30s elapsed]
aws_elasticache_cluster.my-redis: Creation complete after 32s [id=my-redis-cluster]

Apply complete! Resources: 10 added, 0 changed, 0 destroyed.
```

## License

This code is available under the Apache 2.0 license.
