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

# Invoke the Lambda function 3 times every 5 seconds.
for i in {1..3}; do
    echo "Invoking the Lambda function, attempt $i."
    AWS_MAX_ATTEMPTS=1 \
    awslocal lambda invoke \
        --cli-connect-timeout 3600 \
        --cli-read-timeout 3600 \
        --function-name "function_one" \
        --payload "{\"message\": \"Testing Lambda Debug Mode lifting the 1-second timeout for function-one. Attempt $i.\"}" \
        /dev/stdout 2>/dev/stderr &
    sleep 5
done

