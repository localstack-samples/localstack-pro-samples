# LocalStack Demo: MQ Broker

Simple demo application illustrating the use of MQ using LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command runs the example, which starts up a broker and sends a message to a queue:
```
make run
```

After the test script completes, the logs in your terminal should look similar to the output below:
```
$ make run
Creating MQ broker in LocalStack ...
Created MQ broker with id: b-7dc2ba4a-53a0-41ef-a2ad-92eac3ad879d
Describe broker to get the endpoint
Broker endpoint on http://localhost:4510
Sending message to broker
Message sentCleaning up - deleting broker
Deleted Broker b-7dc2ba4a-53a0-41ef-a2ad-92eac3ad879d
```

## License

This code is available under the Apache 2.0 license.
