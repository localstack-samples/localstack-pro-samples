#!/bin/bash
set -e

echo "Step 1: Trying to create Kinesis stream - should get DENIED ..."
awslocal kinesis create-stream --stream-name s1 --shard-count 1

echo "Step 2: Trying to create S3 bucket - should get DENIED ..."
awslocal s3 mb s3://test-iam-bucket
list_result=$(awslocal s3api list-buckets | jq -r .Buckets)
../assert "$list_result" = []

echo "Step 3: Creating user with IAM policy to allow Kinesis access ..."
pol_arn=$(awslocal iam create-policy --policy-name p1 --policy-document '{"Version":"2012-10-17","Statement":[{"Sid":"pol123","Effect":"Allow","Action":["kinesis:*","s3:*"],"Resource":"*"}]}' | jq -r '.Policy.Arn')
awslocal iam create-user --user-name user1 | grep UserName
test $pol_arn && awslocal iam attach-user-policy --user-name user1 --policy-arn $pol_arn
keys=$(awslocal iam create-access-key --user-name user1 | jq '.AccessKey')
accessKey=$(echo $keys | jq -r '.AccessKeyId')
secretKey=$(echo $keys | jq -r '.SecretAccessKey')

echo
echo "Done creating IAM users - now trying to create the same resources as above using \
the generated IAM credentials (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY) and associated policy"
echo

export AWS_ACCESS_KEY_ID=$accessKey
export AWS_SECRET_ACCESS_KEY=$secretKey

echo "Step 4: Trying to create Kinesis stream using IAM credentials - should get ALLOWED ..."
awslocal kinesis create-stream --stream-name s1 --shard-count 1
awslocal kinesis describe-stream --stream-name s1 | grep StreamStatus

echo "Step 5: Trying to create S3 bucket using IAM credentials - should get ALLOWED ..."
awslocal s3 mb s3://test-iam-bucket
