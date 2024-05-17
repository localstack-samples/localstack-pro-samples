# LocalStack Demo: Lambda Layers

Simple demo application illustrating Lambda layers using LocalStack, deployed via the Serverless framework.

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

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

Deploy the app locally and run a Lambda test invocation:
```
make run
```

You should see a success output in the terminal:
```
{
    "StatusCode": 200
}
```

... and your LocalStack container should contain output similar to this:
```
>START RequestId: ba4efc87-7bf9-1705-9f45-8e84ba8eb071 Version: $LATEST
> 2019-10-23T14:25:12.709Z	ba4efc87-7bf9-1705-9f45-8e84ba8eb071	INFO	This text should be printed in the Lambda
> END RequestId: ba4efc87-7bf9-1705-9f45-8e84ba8eb071
> REPORT RequestId: ba4efc87-7bf9-1705-9f45-8e84ba8eb071	Duration: 22.65 ms	Billed Duration: 100 ms	Memory Size: 1536 MB	Max Memory Used: 42 MB
```

## License

This code is available under the Apache 2.0 license.
