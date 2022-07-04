# LocalStack Demo: Basic IoT Entities

Simple demo application illustrating usage of IoT APIs in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`

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

Deploy the app locally and run a Lambda test invocation:
```
make run
```

You should see a couple of successful API call outputs in the terminal:
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

The example then also connects to the IoT MQTT endpoint and sends/receives a couple of messages, see the exemplary output below:
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
