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

## App Details

Please refer to the `templates/` folder for details about the CloudFormation templates for the ECS service.

## Running

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=cloudformation,ecs,ec2 localstack start
```

Deploy the app locally via CloudFormation:
```
make deploy
```

You should see some logs and a success output in the terminal:
```
...
Sample app (nginx) successfully deployed.
```

Finally, the test app (nginx) should be accessible under the URL http://localhost:45139/ .

## License

This code is available under the Apache 2.0 license.
