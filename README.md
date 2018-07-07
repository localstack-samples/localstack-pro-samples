# test-artifacts
Test files and data used in the LocalStack integration tests

## Lambda
### Go
A test application for the go1.x runtime can be found at `lambda/go1.x/task.zip`
Install using the `aws lambda create-function` api, make sure to use `LAMBDA_EXECUTOR=docker` when starting localstack
and set the task runtime to "go1.x".

Creating the task:
```
$ aws --endpoint-url=http://localhost:4574 lambda create-function --function-name=task --runtime="go1.x" --role=r1 --handler=task --zip-file fileb://task.zip --region=us-east-1
```

Invoking the task:
```
$ aws lambda --endpoint-url=http://localhost:4574 invoke --function-name task --payload='{"Name": "Test"}' --region=us-east-1 result.log; cat result.log
{
    "StatusCode": 200
}
"Hello Test!"
```