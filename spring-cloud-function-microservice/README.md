# Spring Cloud Function on LocalStack [JVM]

This example shows how to use JVM-based project powered by
Spring Cloud Function framework together with LocalStack.

## Covered Topics

Application setup:
* HTTP routing and warmups
* Pure lambda functions
* Event handling lambda functions [pro]

Application testing:
* Testing with JUnit and LocalStack Java Utils
* Debugging application with remote debugger

Deployment setup:
* Deploying and hot code swapping with Serverless
* Deploying and hot code swapping with CDK
* Deploying and hot code swapping with Terraform

## Project Structure

* `src/main` - project sources directory
* `src/test` - project tests directory
* `deployments/cdk` - sample CDK deployment
* `deployments/serverless` - sample Serverless deployment
* `deployments/terraform` - sample Terraform deployment

## Dependencies

* [Docker](https://www.docker.com)
* [Java JDK 11](https://www.oracle.com/java/technologies/downloads/)
* [optional] [watchman](https://facebook.github.io/watchman/) for code hot-swapping
* [optional] [Nodejs](https://nodejs.org/en/) for Serverless deployments
* [optional] [aws cdk](https://www.npmjs.com/package/aws-cdk) and [cdklocal](https://www.npmjs.com/package/aws-cdk-local) for CDK deployments
* [optional] [Terraform](https://www.terraform.io) for terraform deployments

## Command-line Interface

* `make usage` - show usage help

## Quickstart

* If you are going to use pro-features, rename `.env.example`
  to `.env` and set your LocalStack pro API Key
* Start the LocalStack service `docker compose up [-d]`
* Deploy the local stack using one of available frameworks
  `make deploy-<framework>-local`, for example `make deploy-cdk-local`
* Optionally start the watchman service for code hot-swapping
  `make watch`
* Invoke one of the endpoints, or lambda functions

Inspect the `Makefile` and configuration files to see
implementation details.

## Debugging

* create a new shell target to wait debugger server on port `5050`:
```shell
while [[ -z $(docker ps | grep :5050) ]]; do sleep 1; done; sleep 1;
```
* Add a new Remote Debugger target to attach to port `5050` and select
the shell target from above as a `before launch` action
* Run the debugger and invoke your lambda function
