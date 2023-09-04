#!/bin/bash
set -eo pipefail

# hardcode +/-1 day using https://www.unixtimestamp.com/

# HACK: +/ 1h based on now
NOW=$(date -u +%s)
start=$(($NOW-3600))
end=$(($NOW+3600))

awslocal xray get-trace-summaries --start-time=$start --end-time=$end


# hardcoded: update based on previous output
# trace_id=1-dc99d00f-c079a84d433534434534ef0d
# awslocal xray batch-get-traces --trace-ids $trace_id
