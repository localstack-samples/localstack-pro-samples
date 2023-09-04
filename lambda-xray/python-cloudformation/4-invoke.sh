#!/bin/bash
set -eo pipefail
FUNCTION=$(awslocal cloudformation describe-stack-resource --stack-name blank-python --logical-resource-id function --query 'StackResourceDetail.PhysicalResourceId' --output text)

while true; do
  awslocal lambda invoke --function-name $FUNCTION --payload file://event.json out.json
  cat out.json
  echo ""
  sleep 2
done
