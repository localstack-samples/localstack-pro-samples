#!/bin/bash

awslocal lambda create-function \
    --function-name localstack-example \
    --runtime nodejs18.x \
    --role arn:aws:iam::000000000000:role/lambda-ex \
    --code S3Bucket="hot-reload",S3Key="$(PWD)/dist" \
    --handler api.default

function_url=$(awslocal lambda create-function-url-config --function-name localstack-example --auth-type NONE | jq -r '.FunctionUrl')

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30}' \
  "$function_url"

curl -X GET "$function_url"
