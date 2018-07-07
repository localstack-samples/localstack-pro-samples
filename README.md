# test-artifacts
Test files and data used in the LocalStack integration tests

## Lambda
### Go
A test application for the go1.x runtime can be found at `lambda/go1.x/task.zip`
Install using the `aws lambda create-function` api, make sure to use `LAMBDA_EXECUTOR=docker` when starting localstack
and set the task runtime to "go1.x".