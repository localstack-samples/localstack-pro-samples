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
        --runtime python3.9
}

# Function to check the status of a Lambda function
check_lambda_status() {
    local function_name=$1
    local status
    status=$(awslocal lambda get-function --function-name "$function_name" 2>&1)
    # Check if "Active" is in the response
    if echo "$status" | grep -q "Active"; then
        return 0
    fi
    return 1
}

# Create and invoke Lambda functions in parallel
for function_name in "${FUNCTION_NAMES[@]}"; do
    create_lambda_function "$function_name" &
done

# Wait for all Lambda functions to be created
wait

echo "Waiting for Lambda functions to become active..."

for function_name in "${FUNCTION_NAMES[@]}"; do
    while true; do
        if check_lambda_status "$function_name"; then
            echo "Lambda function $function_name is active."
            break
        else
            echo "Lambda function $function_name is still pending. Waiting..."
            sleep 1
        fi
    done
done

# Invoke the Lambda functions in parallel
for function_name in "${FUNCTION_NAMES[@]}"; do
    echo "Invoking the Lambda function $function_name."
    awslocal lambda invoke \
        --function-name "$function_name" \
        test.${function_name}.lambda.log \
        --payload '{"message": "Testing Lambda Debug Mode lifting the 1-second timeout for '"$function_name"'. "}' &
done

# Wait for all invocations to complete
wait

echo "All Lambda functions have been invoked."

