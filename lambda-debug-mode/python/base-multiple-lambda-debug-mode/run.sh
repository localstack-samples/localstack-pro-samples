#!/bin/bash

# Define the names of the Lambda functions
FUNCTION_NAMES=("function_one" "function_two")

# Function to create a Lambda function
create_lambda_function() {
    local function_name=$1
    local handler="handler_${function_name}.handler"
    echo "Creating Lambda function $function_name with handler $handler through hot-reload with one second timeout."
    awslocal lambda create-function \
        --function-name "$function_name" \
        --timeout 1 \
        --code "S3Bucket=hot-reload,S3Key=$(pwd)/" \
        --handler "$handler" \
        --role arn:aws:iam::000000000000:role/test-role \
        --runtime python3.12
}

# Create and invoke Lambda functions in parallel
for function_name in "${FUNCTION_NAMES[@]}"; do
    create_lambda_function "$function_name" &
done

# Wait for all Lambda functions to be created
wait

echo "Waiting for Lambda functions to become active..."
for function_name in "${FUNCTION_NAMES[@]}"; do
    awslocal lambda wait function-active-v2 --function-name "$function_name"
done

# Invoke the Lambda functions in parallel
for function_name in "${FUNCTION_NAMES[@]}"; do
    echo "Invoking the Lambda function $function_name."
    AWS_MAX_ATTEMPTS=1 \
    awslocal lambda invoke \
        --cli-connect-timeout 3600 \
        --cli-read-timeout 3600 \
        --function-name "$function_name" \
        --payload '{"message": "Testing Lambda Debug Mode lifting the 1-second timeout for '"$function_name"'. "}' \
        /dev/stdout 2>/dev/stderr &
done

# Wait for all invocations to complete
wait

echo "All Lambda functions have been invoked."

echo "Set a breakpoint and attach the Python remote debugger from your IDE"
