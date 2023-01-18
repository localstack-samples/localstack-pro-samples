#!/bin/bash

awslocal lambda create-function --function-name func1 --timeout 60 --code "S3Bucket=__local__,S3Key=$(pwd)/" --handler handler.handler --role r1 --runtime python3.7
awslocal lambda invoke --function-name func1 test.lambda.log --payload '{"message":"Hello from LocalStack!"}'
