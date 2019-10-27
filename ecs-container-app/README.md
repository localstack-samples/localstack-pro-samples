# LocalStack Demo: ECS Container App

Simple demo application illustrating ECS applications running locally using LocalStack.

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

Deploy the app locally and run a test invocation:
```
make deploy
```

You should see a success output in the terminal:
```
{
    "StatusCode": 200
}
```

... and your LocalStack container should contain output similar to this:
```

```

## License

This code is available under the Apache 2.0 license.
