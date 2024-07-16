# Using filters to process all events with DynamoDB and Lambda

This example demonstrates how to create a Lambda trigger to process a stream from a DynamoDB table. This example will demonstrate the following workflow:

- A user writes an item to a DynamoDB table. Each item in the table represents a bark.
- A new stream record reflects that a new item has been added to the DynamoDB table.
- The new stream record triggers a Lambda function.
- If the stream record indicates that a new item was added to the DynamoDB table, the Lambda function reads the data from the stream record and publishes a message to a topic in SNS.
- The message is received by subscribers to the SNS topic.

## Prerequisites

* LocalStack
* Docker
* `awslocal` CLI
* `jq`

## Start LocalStack

Start LocalStack using the following command:

```bash
localsatck start
```

## Create a DynamoDB table with a stream enabled

Create a DynamoDB table (`BarkTable`) to store all of the barks from Woofer users. The primary key is composed of `Username` (partition key) and `Timestamp` (sort key). `BarkTable` has a stream enabled.

```bash
awslocal dynamodb create-table \
    --table-name BarkTable \
    --attribute-definitions AttributeName=Username,AttributeType=S AttributeName=Timestamp,AttributeType=S \
    --key-schema AttributeName=Username,KeyType=HASH  AttributeName=Timestamp,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES
```

Fetch the ARN of the stream from the DynamoDB table:

```bash
export latest_stream_arn=$(awslocal dynamodb describe-table --table-name BarkTable --query 'Table.LatestStreamArn' --output text)
```

## Create a Lambda execution role

Create a `WooferLambdaRole` IAM role using the policy defined in the `trust-relationship.json` file. Run the following command to create the role:

```bash
awslocal iam create-role --role-name WooferLambdaRole \
    --path "/service-role/" \
    --assume-role-policy-document file://trust-relationship.json
```

Enter the following command to attach the policy defined in the `role-policy.json` document to `WooferLambdaRole`:

```bash
awslocal iam put-role-policy --role-name WooferLambdaRole \
    --policy-name WooferLambdaRolePolicy \
    --policy-document file://role-policy.json
```

## Create a SNS topic

Enter the following command to create a new SNS topic:

```bash
awslocal sns create-topic --name wooferTopic
```

Enter the following command to subscribe an email address to `wooferTopic`:

```bash
awslocal sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:000000000000:wooferTopic \
    --protocol email \
    --notification-endpoint user1@yourdomain.com
```

You can customize the notification endpoint to your own preference.

## Create and test a Lambda function

We have defined a Lambda function `publishNewBark` to process stream records from `BarkTable`.

Create a zip file to contain `publishNewBark.js`:

```bash
zip publishNewBark.zip publishNewBark.js
```

Create the Lambda function:

```bash
awslocal lambda create-function \
    --region us-east-1 \
    --function-name publishNewBark \
    --zip-file fileb://publishNewBark.zip \
    --role arn:aws:iam::000000000000:role/service-role/WooferLambdaRole \
    --handler publishNewBark.handler \
    --timeout 15 \
    --runtime nodejs16.x
```

Enter the following command to test the `publishNewBark` function:

```bash
awslocal lambda invoke \
    --function-name publishNewBark \
    --payload file://payload.json \
    --cli-binary-format raw-in-base64-out output.txt
```

If the test was successful, you will see the following output:

```bash
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
```

In addition, the output.txt file will contain the following text.

```txt
"Successfully processed 1 records."
```

## Create and test a trigger

Enter the following command to create the trigger:

```bash
awslocal lambda create-event-source-mapping \
    --region us-east-1 \
    --function-name publishNewBark \
    --event-source arn:aws:dynamodb:us-east-1:000000000000:table/BarkTable/stream/2023-07-09T12:00:13.312  \
    --batch-size 1 \
    --starting-position TRIM_HORIZON
```

Replace the `event-source` value with the value of `latest_stream_arn` that you saved earlier.

Run the following command to test the trigger:

```bash
awslocal dynamodb put-item \
    --table-name BarkTable \
    --item Username={S="Jane Doe"},Timestamp={S="2016-11-18:14:32:17"},Message={S="Testing...1...2...3"}
```

You should receive a new message on your notification endpoint within a few minutes.

The Lambda function processes only new items that you add to `BarkTable`. If you update or delete an item in the table, the function does nothing.
