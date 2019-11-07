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

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=cloudformation,iot localstack start
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

## License

This code is available under the Apache 2.0 license.
