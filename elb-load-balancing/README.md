# LocalStack Demo: ELB Application Load Balancers

Simple demo application illustrating ELBv2 Application Load Balancers using LocalStack, deployed via the Serverless framework.

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

Deploy the app locally and run an ELB Lambda test invocation:
```
make run
```

You should see some output with the deployment logs of the Serverless application, and finally two successful invocations of the ELB endpoints `/hello1` and `/hello2`:
```
> sls deploy --stage local
...
Serverless app successfully deployed. Now trying to invoke the Lambda functions via ELB endpoint.
...
Invoking endpoint 1: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello1
"Hello 1"
Invoking endpoint 2: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello2
"Hello 2"
```

## License

This code is available under the Apache 2.0 license.
