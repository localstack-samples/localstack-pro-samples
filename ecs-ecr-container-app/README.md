# LocalStack Demo: ECS Container App

Simple demo application illustrating ECS applications running locally using LocalStack. The application image is built using Docker and pushed to a local ECR registry.

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

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command builds and deploys the app locally via CloudFormation:

```
make deploy
```

Specifically, the script above runs the following steps:
1. Create a new ECR registry locally
2. Build the application Docker image (from the `nginx` base image)
3. Push the image to the ECR registry
4. Create the ECS cluster and infrastructure
5. Create and deploy the ECS application, which starts the container in you local Docker environment

You should see some logs and a success output in the terminal:
```
...
Sample app (nginx) successfully deployed.
```

Finally, the test app (nginx) should be accessible under the URL http://localhost:45139/ .

## License

This code is available under the Apache 2.0 license.
