# Localstack Demo: Access S3 resources from different account and different region

## Profiles

The following profiles will have to be created:

* Profile `ls-a-admin`: admin user of account A.

* Profile `ls-b-admin`: admin user of account B.

* Profile `ls-a`: account A user that creates the S3 bucket and afferent resources inside the bucket.

* Profile `ls-b`: account B user that copies the resources from account A user's S3 bucket into a bucket it owns.

## Create Users

Create the following profiles in `~/.aws/config`:

```
[profile ls-a-admin]
region=us-east-1
output=json
endpoint_url=https://localhost.localstack.cloud:4566

[profile ls-b-admin]
region=eu-central-1
output=json
endpoint_url=https://localhost.localstack.cloud:4566
```

The `~/.aws/credentials` would initially look as follows:

```
[ls-a-admin]
aws_access_key_id=000000000001
aws_secret_access_key=test

[ls-b-admin]
aws_access_key_id=000000000002
aws_secret_access_key=test
```

Then, create the actual `ls-a` and `ls-b` users:

```shell
aws iam create-user --user-name ls-a --profile ls-a-admin
aws iam create-user --user-name ls-b --profile ls-b-admin
```

The following outputs would be returned:

```shell
localstack@macintosh serverless-data-processing-pipeline % aws iam create-user --user-name ls-a --profile ls-a-admin           
{
    "User": {
        "Path": "/",
        "UserName": "ls-a",
        "UserId": "m963bjpmc9sh0khhd9co",
        "Arn": "arn:aws:iam::000000000001:user/ls-a",
        "CreateDate": "2024-06-19T16:57:16.763000Z"
    }
}
localstack@macintosh serverless-data-processing-pipeline % aws iam create-user --user-name ls-b --profile ls-b-admin
{
    "User": {
        "Path": "/",
        "UserName": "ls-b",
        "UserId": "juo7catmp7dj7y66kk3g",
        "Arn": "arn:aws:iam::000000000002:user/ls-b",
        "CreateDate": "2024-06-19T17:04:34.649000Z"
    }
}
```

## Attach Policy to Users

Create policies `pa` and `pb` for user A and respectively user B:

```shell
aws iam create-policy --policy-name pa --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"}]}' --profile ls-a-admin 
aws iam create-policy --policy-name pb --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"}]}' --profile ls-b-admin 
```

```shell
localstack@macintosh serverless-data-processing-pipeline % aws iam create-policy --policy-name pa --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"}]}' --profile ls-a-admin 
{
    "Policy": {
        "PolicyName": "pa",
        "PolicyId": "A9LSZ6ZQ1IZPK4CI9S5AJ",
        "Arn": "arn:aws:iam::000000000001:policy/pa",
        "Path": "/",
        "DefaultVersionId": "v1",
        "AttachmentCount": 0,
        "CreateDate": "2024-06-19T17:09:44.758000Z",
        "UpdateDate": "2024-06-19T17:09:44.758000Z",
        "Tags": []
    }
}
localstack@macintosh serverless-data-processing-pipeline % aws iam create-policy --policy-name pb --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"}]}' --profile ls-b-admin
{
    "Policy": {
        "PolicyName": "pb",
        "PolicyId": "AMAKM9JGV5WB9NWZP218Q",
        "Arn": "arn:aws:iam::000000000002:policy/pb",
        "Path": "/",
        "DefaultVersionId": "v1",
        "AttachmentCount": 0,
        "CreateDate": "2024-06-19T17:09:54.443000Z",
        "UpdateDate": "2024-06-19T17:09:54.443000Z",
        "Tags": []
    }
}
```

And then attach said policies to each user:

```shell
aws iam attach-user-policy --user-name ls-a --policy-arn arn:aws:iam::000000000001:policy/pa --profile ls-a-admin
aws iam attach-user-policy --user-name ls-b --policy-arn arn:aws:iam::000000000002:policy/pb --profile ls-b-admin
```

## Create User Profiles

Generate the AWS keys for each respective user:

```shell
aws iam create-access-key --user-name ls-a --profile ls-a-admin
aws iam create-access-key --user-name ls-b --profile ls-b-admin
```

```shell
localstack@macintosh serverless-data-processing-pipeline % aws iam create-access-key --user-name ls-a --profile ls-a-admin
{
    "AccessKey": {
        "UserName": "ls-a",
        "AccessKeyId": "LKIAQAAAAAAA4ZFEPLMV",
        "Status": "Active",
        "SecretAccessKey": "NV/Uft4BtS1ZgnXOOFvYc+xKZj921lCbDRducl9N",
        "CreateDate": "2024-06-19T17:16:59Z"
    }
}
localstack@macintosh serverless-data-processing-pipeline % aws iam create-access-key --user-name ls-b --profile ls-b-admin
{
    "AccessKey": {
        "UserName": "ls-b",
        "AccessKeyId": "LKIAQAAAAAABCYRWOBQD",
        "Status": "Active",
        "SecretAccessKey": "/asqAjMJvpFt/dHeGW7ILG8ZZQGQLabx2KOtILRp",
        "CreateDate": "2024-06-19T17:17:05Z"
    }
}
```

And then create the respective `ls-a` and `ls-b` profiles in `~/.aws/config` and `~/.aws/credentials` based on each user's access key id and secret access key:

```text
[profile ls-a]
region=us-east-1
output=json
endpoint_url=https://localhost.localstack.cloud:4566

[profile ls-b]
region=eu-central-1
output=json
endpoint_url=https://localhost.localstack.cloud:4566
```

Finally, verify that listing S3 buckets works:

```shell
aws s3 ls --profile ls-a
aws s3 ls --profile ls-b
```

## Create S3 Resource in Account A

Create the S3 bucket and add a few objects to the bucket:

```shell
aws s3 mb s3://source --profile ls-a
aws s3 sync ./bucket s3://source --profile ls-a
```

## Attach Bucket Policy

Let's attach a bucket policy to the bucket in account A that allows user from account B to access the objects on said bucket:

```shell
aws s3api put-bucket-policy --bucket source --policy file://source_bucket_policy.json --profile ls-a
```

Where `source_bucket_policy.json` would look like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*"
            ],
            "Principal": { "AWS": "arn:aws:iam::000000000002:user/ls-b" },
            "Resource": "arn:aws:s3:::source/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:List*"
            ],
            "Principal": { "AWS": "arn:aws:iam::000000000002:user/ls-b" },
            "Resource": "arn:aws:s3:::source"
        }
    ]
}

```
