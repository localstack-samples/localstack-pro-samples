#!/bin/bash
set -eo pipefail

# AWS X-Ray documentation: https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html
# * Concepts: https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html
# * Getting data: https://docs.aws.amazon.com/xray/latest/devguide/xray-api-gettingdata.html
# * Segment documents schema: https://docs.aws.amazon.com/xray/latest/devguide/xray-api-segmentdocuments.html

# Retrieve traces for the last 10 minutes by default
num_seconds=${1-600}

# X-Ray time is always based on UTC, therefore using -u
# Helpful UNIX timestamp converter for hardcoding: https://www.unixtimestamp.com/
EPOCH=$(date -u +%s)
start=$(($EPOCH-600))
end=$(($EPOCH))

# Retrieve trace summaries
awslocal xray get-trace-summaries --start-time=$start --end-time=$end

# Retrive full traces
TRACEIDS=$(awslocal xray get-trace-summaries --start-time=$start --end-time=$end --query 'TraceSummaries[*].Id' --output text)
awslocal xray batch-get-traces --trace-ids $TRACEIDS --query 'Traces[*]'
