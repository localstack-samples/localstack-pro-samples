#!/bin/bash
set -euxo pipefail
export AWS_SECRET_ACCESS_KEY=test

# Create `ls-a` and `ls-b` IAM users using the root accounts of each user
AWS_ACCESS_KEY_ID=000000000001 awslocal iam create-user --user-name ls-a
AWS_ACCESS_KEY_ID=000000000002 awslocal iam create-user --user-name ls-b

# Create IAM policies for each of the IAM users using the root accounts of each user
AWS_ACCESS_KEY_ID=000000000001 awslocal iam create-policy --policy-name pa --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"}]}'
AWS_ACCESS_KEY_ID=000000000002 awslocal iam create-policy --policy-name pb --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"}]}'

# Attach the IAM policies to each IAM user using the root accounts of each user 
AWS_ACCESS_KEY_ID=000000000001 awslocal iam attach-user-policy --user-name ls-a --policy-arn arn:aws:iam::000000000001:policy/pa
AWS_ACCESS_KEY_ID=000000000002 awslocal iam attach-user-policy --user-name ls-b --policy-arn arn:aws:iam::000000000002:policy/pb

# Create access keys for each user using the root accounts of each user
CREDENTIALS_A=$(AWS_ACCESS_KEY_ID=000000000001 awslocal iam create-access-key --user-name ls-a)
CREDENTIALS_B=$(AWS_ACCESS_KEY_ID=000000000002 awslocal iam create-access-key --user-name ls-b)

# Retrieve the access key id of each user
# In LocalStack, the secret access key is not strictly enforced
# But the access key id is
USER_ACCESS_KEY_ID_A=`jq -r .AccessKey.AccessKeyId <<< $CREDENTIALS_A`
USER_ACCESS_KEY_ID_B=`jq -r .AccessKey.AccessKeyId <<< $CREDENTIALS_B`

# Create `source` bucket in `ls-a` user's account
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_A awslocal s3 mb s3://source
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_A awslocal s3 sync ./bucket s3://source

# Attach a bucket policy so that user `ls-b` can access it
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_A awslocal s3api put-bucket-policy --bucket source --policy file://source_bucket_policy.json

# Attempt to access bucket `source` using `ls-a` user
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_B awslocal s3 ls s3://source
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_B awslocal s3api list-object-versions --bucket source --prefix main.go

# Sync buckets `source` and `target` using `ls-b` user
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_B awslocal s3 mb s3://target
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_B awslocal s3 sync s3://source s3://target
AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_B awslocal s3api list-object-versions --bucket target --prefix main.go

# Fail the script if somehow user A can access the resources of bucket `target`
echo "Check if s3api list-object-versions commnands fails as expected"
if AWS_ACCESS_KEY_ID=$USER_ACCESS_KEY_ID_A awslocal s3api list-object-versions --bucket target --prefix main.go; then
    exit 1
fi
