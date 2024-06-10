#!/bin/bash
set -euo pipefail

invoke_endpoints() {
  echo "Invoking endpoint 1: http://test.example.com:4566/hello"
  response1=$(curl -H 'Host: test.example.com' http://localhost:4566/hello)
  if [ "$response1" != "hello world" ]; then
    echo "Error: Response from endpoint 1 does not match expected output."
    exit 1
  fi

  echo "Invoking endpoint 2: http://test.example.com:4566/goodbye"
  response2=$(curl -H 'Host: test.example.com' http://localhost:4566/goodbye)
  if [ "$response2" != "goodbye" ]; then
    echo "Error: Response from endpoint 2 does not match expected output."
    exit 1
  fi
}

target="${target:-default}"

if [[ "$target" == "ci" ]]; then
  invoke_endpoints
else
  echo "Now trying to invoke the API Gateway endpoints with custom domains."
  echo "Sample command to invoke endpoint 1:"
  echo "curl -H 'Host: test.example.com' http://localhost:4566/hello"
  echo "Sample command to invoke endpoint 2:"
  echo "curl -H 'Host: test.example.com' http://localhost:4566/goodbye"
fi
