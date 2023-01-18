#!/bin/bash

awslocal lambda create-function \
    --function-name localstack-nodejs-lambda-function \
    --code S3Bucket="hot-reload",S3Key="$(pwd)/" \
    --handler function.handler \
    --runtime nodejs14.x \
    --timeout 120 \
    --role arn:aws:iam::000000000000:role/lambda-role

awslocal lambda invoke \
    --function-name localstack-nodejs-lambda-function test.lambda.log \
    --cli-binary-format raw-in-base64-out \
    --payload '{"hello":"world"}'
