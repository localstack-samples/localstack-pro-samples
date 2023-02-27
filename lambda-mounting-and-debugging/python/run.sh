#!/bin/bash

awslocal lambda create-function --function-name func1 --timeout 60 --code "S3Bucket=hot-reload,S3Key=$(pwd)/" --handler handler.handler --role arn:aws:iam::000000000000:role/test-role --runtime python3.9
awslocal lambda invoke --function-name func1 test.lambda.log --payload '{"message":"Hello from LocalStack!"}'
