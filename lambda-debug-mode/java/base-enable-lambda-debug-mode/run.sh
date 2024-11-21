#!/bin/bash
#
# Set the name of the Lambda function.
FUNCTION_NAME="function-one"

# Create the Lambda function 'function-one' with one second timeout.
echo "Creating Lambda function $FUNCTION_NAME with one second timeout."
awslocal lambda create-function \
    --function-name $FUNCTION_NAME\
    --runtime java17 \
    --role arn:aws:iam::000000000000:role/test-role \
    --handler LambdaFunctionHandler \
    --zip-file fileb://java-function/build/distributions/base-enable-lambda-debug-mode.zip \
    --timeout 1 \
    --memory-size 512 \
    --environment '{"Variables": {"_JAVA_OPTIONS": "-Xshare:off -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=0.0.0.0:5050"}}'

awslocal lambda wait function-active-v2 --function-name "$FUNCTION_NAME"

# Invoke the Lambda function.
echo "Invoking the Lambda function."
AWS_MAX_ATTEMPTS=1 \
awslocal lambda invoke \
    --cli-connect-timeout 3600 \
    --cli-read-timeout 3600 \
    --function-name "$FUNCTION_NAME" \
    --payload '{"message": "Testing Lambda Debug Mode lifting the 1-second timeout for function-one."}' \
    /dev/stdout 2>/dev/stderr

echo "Set a breakpoint and attach the Python remote debugger from your IDE"
