# AppSync GraphQL API

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | AppSync, DynamoDB, RDS              |
| Integrations | AWS SDK, AWS CLI                    |
| Categories   | GraphQL; Serverless                 |

## Introduction

A demo application illustrating how to proxy data from different resources (DynamoDB tables, RDS Aurora Postgres databases) via AppSync GraphQL using LocalStack. The sample runs mutation and query operations for two data sources and demonstrates real-time notifications via WebSocket subscriptions.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Python 3](https://www.python.org/downloads/)

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Start LocalStack

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script:

- Deploys AppSync GraphQL API with DynamoDB and RDS Aurora Postgres resolvers.
- Runs mutation queries to insert items into both data sources.
- Runs query operations to scan and return items from DynamoDB and RDS Aurora.
- Connects a WebSocket client to verify real-time subscription notifications.

You should see a success output in the terminal:

```bash
{"data":{"addPostDDB":{"id":{"S":"id123"}}}}
{"data":{"getPostsDDB":[{"id":{"S":"id123"}}]}}
...
{"data":{"addPostRDS":{"id":{"S":"id123"}}}}
{"data":{"getPostsRDS":[{"id":{"S":"id123"}}]}}
```

The item should also have been added to your local DynamoDB table:

```bash
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

Finally, you should see a notification from the WebSocket client:

```bash
Starting a WebSocket client to subscribe to GraphQL mutation operations.
Connecting to WebSocket URL ws://localhost:4510/graphql/...
...
Received notification message from WebSocket: {"addedPost": {"id": "id123"}}
```

## License

This code is available under the Apache 2.0 license.
