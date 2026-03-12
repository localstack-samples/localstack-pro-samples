# IoT Basics

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | IoT                                 |
| Integrations | AWS CLI                             |
| Categories   | IoT                                 |

## Introduction

A demo application illustrating basic IoT API usage with LocalStack. The sample creates IoT things, policies, and certificates, then connects to the IoT MQTT endpoint to publish and subscribe to messages — all locally without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)

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

The script creates IoT things and policies, connects to the local MQTT endpoint, publishes messages, and verifies they are received by a subscriber.

You should see IoT API call outputs:

```
{
    "things": [
        {
            "thingName": "thing1",
            "thingArn": "arn:aws:iot:us-east-1:000000000000:thing/thing1",
            "attributes": {
                "attr1": "value1",
                "attr2": "value2"
            }
        }
    ]
}
{
    "policies": [
        {
            "policyName": "pol1",
            "policyArn": "arn:aws:iot:us-east-1:000000000000:policy/pol1"
        }
    ]
}
...
```

The example then connects to the IoT MQTT endpoint and sends/receives messages:

```
Running MQTT publish/subscribe test
10 messages published
0: /test-topic => b'TEST MESSAGE 0'
1: /test-topic => b'TEST MESSAGE 1'
2: /test-topic => b'TEST MESSAGE 2'
3: /test-topic => b'TEST MESSAGE 3'
4: /test-topic => b'TEST MESSAGE 4'
5: /test-topic => b'TEST MESSAGE 5'
6: /test-topic => b'TEST MESSAGE 6'
7: /test-topic => b'TEST MESSAGE 7'
8: /test-topic => b'TEST MESSAGE 8'
9: /test-topic => b'TEST MESSAGE 9'
```

## License

This code is available under the Apache 2.0 license.
