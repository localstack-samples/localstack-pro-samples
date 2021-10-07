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

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=serverless,sns,sqs,elasticache,es,rds localstack start
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

aws_api_gateway_rest_api.demo: Creating...
aws_iam_role.lambda: Creating...
aws_iam_role.invocation_role: Creating...
aws_elasticache_cluster.my-redis: Creating...
aws_s3_bucket.testBucket: Creating...
aws_elasticsearch_domain.example: Creating...
aws_iam_role.lambda: Creation complete after 0s [id=demo-lambda]
aws_iam_role.invocation_role: Creation complete after 0s [id=api_gateway_auth_invocation]
aws_lambda_function.authorizer: Creating...
aws_api_gateway_rest_api.demo: Creation complete after 0s [id=fboao5ctp1]
aws_iam_role_policy.invocation_policy: Creating...
aws_iam_role_policy.invocation_policy: Creation complete after 1s [id=api_gateway_auth_invocation:default]
aws_s3_bucket.testBucket: Creation complete after 1s [id=myBucket]
aws_lambda_function.authorizer: Creation complete after 6s [id=api_gateway_authorizer]
aws_api_gateway_authorizer.demo: Creating...
aws_api_gateway_authorizer.demo: Creation complete after 0s [id=4dcdc808]
...
Apply complete! Resources: 9 added, 0 changed, 0 destroyed.
```

## License

This code is available under the Apache 2.0 license.
