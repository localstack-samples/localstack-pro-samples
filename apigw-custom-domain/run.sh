#!/bin/bash
set -euo pipefail

invoke_endpoints() {
  echo "Invoking endpoint 1: http://test.example.com:4566/hello"
  response1=$(curl -H 'Host: test.example.com' http://localhost:4566/hello)
  ../assert "$response1" = "hello world"

  echo "Invoking endpoint 2: http://test.example.com:4566/goodbye"
  response2=$(curl -H 'Host: test.example.com' http://localhost:4566/goodbye)
  ../assert "$response2" = "goodbye"
}

if [[ "$target" == "ci" ]]; then
  invoke_endpoints
else
  echo "Now trying to invoke the API Gateway endpoints with custom domains."
  echo "Sample command to invoke endpoint 1:"
  echo "curl -H 'Host: test.example.com' http://localhost:4566/hello"
  echo "Sample command to invoke endpoint 2:"
  echo "curl -H 'Host: test.example.com' http://localhost:4566/goodbye"
fi
