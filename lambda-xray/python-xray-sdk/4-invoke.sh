#!/bin/bash
set -eo pipefail
FUNCTION=$(awslocal cloudformation describe-stack-resource --stack-name blank-python --logical-resource-id function --query 'StackResourceDetail.PhysicalResourceId' --output text)

### Usage: ./4-invoke.sh NUM (default: 1)

# Store the number passed as an argument
num=${1-1}

# Check if the argument is a positive integer
if ! [[ $num =~ ^[0-9]+$ ]] || [ $num -lt 1 ]; then
  echo "Please provide a positive integer as an argument."
  exit 1
fi

# Loop NUM times
for ((i = 1; i <= num; i++)); do
  awslocal lambda invoke --function-name $FUNCTION --payload file://event.json out.json
  cat out.json
  echo ""
  sleep 2
done
