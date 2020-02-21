# LocalStack Demo: AppSync GraphQL DynamoDB Proxy

Simple demo application illustrating how to proxy DynamoDB data via AppSync GraphQL using LocalStack.

## Prerequisites

* LocalStack
* Docker
* Python 3.6+
* `make`

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=serverless,appsync,dynamodb localstack start
```

## Running

Deploy the app locally and run the GraphQL test invocations:
```
make run
```

The demo will run two GraphQL queries:

1. a mutation query which inserts a new item into DynamoDB
2. a query which scans and returns the items from the DynamoDB table

You should see a success output in the terminal:
```
{"data":{"addPost":{"id":{"S":"id123"}}}}
{"data":{"getPosts":[{"id":{"S":"id123"}}]}}
```

... and the item should have been added to your local DynamoDB table:
```
$ awslocal dynamodb scan --table-name table1
{
    "Items": [
        {
            "id": {
                "S": "id123"
            }
        }
    ],
    "Count": 1,
    "ScannedCount": 1,
    "ConsumedCapacity": null
}
```

Finally, you should also see a message printed from the WebSocket client subscribed to notifications from the API:
```
...
Starting a WebSocket client to subscribe to GraphQL mutation operations.
Connecting to WebSocket URL ws://localhost:4510/graphql/...
...
Received notification message from WebSocket: {"addedPost": {"id": "id123"}}
```

## License

This code is available under the Apache 2.0 license.
