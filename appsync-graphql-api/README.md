# LocalStack Demo: AppSync GraphQL DynamoDB Proxy

Simple demo application illustrating how to proxy DynamoDB data via AppSync GraphQL using LocalStack.

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

## License

This code is available under the Apache 2.0 license.
