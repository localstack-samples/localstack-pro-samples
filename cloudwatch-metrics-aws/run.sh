#!/bin/sh


# set your mail here
my_email=test@example.com

echo "using email $my_email for the example"

echo 'creating lambda'
zip failing-lambda.zip failing-lambda.py

awslocal lambda create-function \
    --function-name my-failing-lambda \
    --zip-file fileb://failing-lambda.zip \
    --handler failing-lambda.lambda_handler \
    --runtime python3.8 \
    --role my-role

echo 'creating sns topic'
topic_arn=$(awslocal sns create-topic --name my-topic-alarm | jq -r .TopicArn)
awslocal sns subscribe --topic-arn $topic_arn --protocol email --notification-endpoint $my_email


echo 'creating cloud watch alarm'
awslocal cloudwatch put-metric-alarm \
  --alarm-name my-lambda-alarm \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --dimensions "Name=FunctionName,Value=my-failing-lambda" \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --period 60 \
  --statistic Sum \
  --treat-missing notBreaching \
  --alarm-actions $topic_arn


echo 'invoking lambda...'
awslocal lambda invoke --function-name my-failing-lambda out.txt

state=$(awslocal cloudwatch describe-alarms --alarm-names my-lambda-alarm | jq -r '.MetricAlarms[0].StateValue')
echo 'alarm state should change within the next minute.'
while [ "$state" != ALARM ]; do
  echo 'checking alarm state...'
  sleep 10
  state=$(awslocal cloudwatch describe-alarms --alarm-names my-lambda-alarm | jq -r '.MetricAlarms[0].StateValue')
done

echo ''
echo 'state changed to Alarm. Check your email, notification should have been arrived!'