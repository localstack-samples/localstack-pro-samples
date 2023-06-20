# LocalStack Demo: Deploying Resources via CDK

Simple demo application illustrating deployment of AWS resources using [CDK for Terraform](https://developer.hashicorp.com/terraform/cdktf).

## Prerequisites

* LocalStack
* Docker
* [`cdktf`](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install)
* [Terraform](https://developer.hashicorp.com/terraform/downloads)
* [`pipenv`](https://pipenv.pypa.io/en/latest/)

## Install dependencies

To install the dependencies, run the following command:

```bash
pipenv install
```

## Generate CDK for Terraform

To generate CDK for Terraform constructs for Terraform providers and modules used in the project, run the following command:

```bash
cdktf get
```

To compile and generate Terraform configuration, run the following command:

```bash
cdktf synth
```

The above command will create a folder called `cdktf.out` that contains all Terraform JSON configuration that was generated.

## Deploy the stack

To deploy the stack, run the following command:

```bash
cdktf deploy
```

## Configuration

LocalStack currently does not provide a wrapper (similar to `cdklocal` or `tflocal`) to run CDK for Terraform. Therefore, you need to configure the AWS `provider` to redirect requests to the LocalStack API (`http://localhost:4566` by default), using [Terraform Override mechanism](https://developer.hashicorp.com/terraform/language/files/override). Check the [`localstack_config.py`](./localstack_config.py) file for an example.
