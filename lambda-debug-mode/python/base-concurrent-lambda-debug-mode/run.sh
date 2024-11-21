#!/bin/bash
#
# Set the name of the Lambda function.
FUNCTION_NAME="function-one"

# Create the Lambda function 'function-one' through hot-reload with one second timeout.
echo "Creating Lambda function $FUNCTION_NAME through hot-reload with one second timeout."
awslocal lambda create-function \
    --function-name "$FUNCTION_NAME"\
    --timeout 1 \
    --code "S3Bucket=hot-reload,S3Key=$(pwd)/" \
    --handler handler.handler \
    --role arn:aws:iam::000000000000:role/test-role \
    --runtime python3.12

awslocal lambda wait function-active-v2 --function-name "$FUNCTION_NAME"

echo "Set a breakpoint and attach the Python remote debugger from your IDE"

# Invoke the Lambda function 3 times every 5 seconds.
for i in {1..3}; do
    echo "Invoking the Lambda function, attempt $i."
    AWS_MAX_ATTEMPTS=1 \
    awslocal lambda invoke \
        --cli-connect-timeout 3600 \
        --cli-read-timeout 3600 \
        --function-name "$FUNCTION_NAME" \
        --payload "{\"message\": \"Testing Lambda Debug Mode lifting the 1-second timeout for function-one. Attempt $i.\"}" \
        /dev/stdout 2>/dev/stderr &
    sleep 5
done
