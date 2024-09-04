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
    --runtime python3.9

# Function to check the status of the Lambda function.
check_lambda_status() {
    status=$(awslocal lambda get-function --function-name "$FUNCTION_NAME" 2>&1)
    # Check if "Active" is in the response
    if echo "$status" | grep -q "Active"; then
        return 0
    fi
    return 1
}

# Wait until the Lambda function is active
echo "Waiting for Lambda function to become active..."
while true; do
    if check_lambda_status; then
        echo "Lambda function is active."
        break
    else
        echo "Lambda function is still pending. Waiting..."
        sleep 1
    fi
done

# Invoke the Lambda function.
echo "Invoking the Lambda function."
awslocal lambda invoke \
    --function-name function-one \
    test.lambda.log \
    --payload '{"message": "Testing Lambda Debug Mode lifting the 1-second timeout for function-one."}'

