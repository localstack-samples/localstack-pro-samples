# LocalStack Demo: AppSync GraphQL APIs for DynamoDB and RDS Aurora Postgres

Simple demo application illustrating how to proxy data from different resources (DynamoDB tables, RDS databases) via AppSync GraphQL using LocalStack.

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

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Deploy the app locally and run the GraphQL test invocations:
```
make run
```

The demo will run different GraphQL queries, for two different datasources (DynamoDB / RDS Aurora):

1. a mutation query which inserts a new item into DynamoDB / RDS Aurora
2. a query which scans and returns the items from DynamoDB / RDS Aurora

You should see a success output in the terminal:
```
{"data":{"addPostDDB":{"id":{"S":"id123"}}}}
{"data":{"getPostsDDB":[{"id":{"S":"id123"}}]}}
...
{"data":{"addPostRDS":{"id":{"S":"id123"}}}}
{"data":{"getPostsRDS":[{"id":{"S":"id123"}}]}}
```

... and the item should have been added to your local DynamoDB table (as well as your RDS database):
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
