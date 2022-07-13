# LocalStack Demo: Websockets via API Gateway V2

Simple demo application illustrating API Gateway V2 websocket APIs using LocalStack, deployed via the Serverless framework.

## Prerequisites

* LocalStack
* Docker
* Node.js / `npm`
* `make`

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Deploy the app locally and send a test message to the created Websockets API.
```
make run
```

This should trigger a Lambda invocation which simply writes the invocation payload back to the websocket. You should see a successful output in the terminal:
```
...
Serverless: Stack create finished...
...
Starting client that connects to Websocket API
Sending message to websocket
Received message from websocket: {"action":"test-action"}
```

## License

This code is available under the Apache 2.0 license.
