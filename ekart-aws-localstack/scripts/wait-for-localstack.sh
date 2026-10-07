#!/bin/bash
echo "Waiting for LocalStack to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:4566/_localstack/health > /dev/null; then
        echo "LocalStack is ready!"
        exit 0
    fi
    echo "Attempt $((attempt + 1))/$max_attempts: LocalStack not ready yet..."
    sleep 2
    attempt=$((attempt + 1))
done
echo "LocalStack failed to start after $max_attempts attempts"
exit 1
