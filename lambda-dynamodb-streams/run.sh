#!/bin/bash

awslocal dynamodb create-table \
    --table-name BarkTable \
    --attribute-definitions AttributeName=Username,AttributeType=S AttributeName=Timestamp,AttributeType=S \
    --key-schema AttributeName=Username,KeyType=HASH  AttributeName=Timestamp,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES

latest_stream_arn=$(awslocal dynamodb describe-table --table-name BarkTable --query 'Table.LatestStreamArn' --output text)

awslocal iam create-role --role-name WooferLambdaRole \
    --path "/service-role/" \
    --assume-role-policy-document file://trust-relationship.json

awslocal iam put-role-policy --role-name WooferLambdaRole \
    --policy-name WooferLambdaRolePolicy \
    --policy-document file://role-policy.json

awslocal sns create-topic --name wooferTopic

awslocal sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:000000000000:wooferTopic \
    --protocol email \
    --notification-endpoint user1@yourdomain.com

awslocal lambda create-function \
    --region us-east-1 \
    --function-name publishNewBark \
    --zip-file fileb://publishNewBark.zip \
    --role arn:aws:iam::000000000000:role/service-role/WooferLambdaRole \
    --handler publishNewBark.handler \
    --timeout 15 \
    --runtime nodejs16.x

awslocal lambda invoke \
    --function-name publishNewBark \
    --payload file://payload.json \
    --cli-binary-format raw-in-base64-out output.txt

awslocal lambda create-event-source-mapping \
    --region us-east-1 \
    --function-name publishNewBark \
    --event-source arn:aws:dynamodb:us-east-1:000000000000:table/BarkTable/stream/2023-07-09T12:00:13.312  \
    --batch-size 1 \
    --starting-position TRIM_HORIZON

awslocal dynamodb put-item \
    --table-name BarkTable \
    --item Username={S="Jane Doe"},Timestamp={S="2016-11-18:14:32:17"},Message={S="Testing...1...2...3"}
