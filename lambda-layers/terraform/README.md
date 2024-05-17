# Lambda Layers with Terraform

Simple demo application illustrating Lambda layers using LocalStack, deployed via Terraform.

## Prerequisites

* LocalStack
* Docker
* Terraform & `tflocal`
* Python & `pip`
* `make`

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started:

```
LOCALSTACK_AUTH_TOKEN=... DEBUG=1 localstack start
```

Deploy the app locally and run a Lambda test invocation:

```
make run
```

You should see a success output in the terminal:
```
{"status": "success"}
```

... and your LocalStack container should contain output similar to this:

```
2024-05-17T15:46:22.870 DEBUG --- [et.reactor-1] l.s.l.i.version_manager    : [my-lambda-function-52785b61-d14d-4871-8074-d5ab5fc49bb1] REPORT RequestId: 52785b61-d14d-4871-8074-d5ab5fc49bb1	Duration: 20.65 ms	Billed Duration: 21 ms	Memory Size: 128 MBMax Memory Used: 128 MB	
2024-05-17T15:46:22.872 DEBUG --- [et.reactor-1] l.s.lambda_.provider       : Lambda invocation duration: 2230.03ms
2024-05-17T15:46:22.874  INFO --- [et.reactor-1] localstack.request.aws     : AWS lambda.Invoke => 200
```

## License

This code is available under the Apache 2.0 license.
