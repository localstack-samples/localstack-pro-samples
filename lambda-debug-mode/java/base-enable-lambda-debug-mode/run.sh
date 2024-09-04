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
    --zip-file fileb://java-lambda-function/base-enable-lambda-debug-mode/build/distributions/base-enable-lambda-debug-mode.zip \
    --timeout 1 \
    --memory-size 512 \
    --environment '{"Variables": {"_JAVA_OPTIONS": "-Xshare:off -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=0.0.0.0:5050"}}'

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

