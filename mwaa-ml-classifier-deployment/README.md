# Localstack Demo: Training and deploying ML classifier with MWAA

App that creates a DAG inside MWAA that takes a dataset, and builds a classifier model based on the feature columns and targetting column. A classifier is trained and the one with the best accuracy out of a bunch of three algorithms is picked up: SVM, Logistic Regression, and Decision Tree. Finally, the model is deployed as a Lambda function.

To keep it simple, no external dependencies (custom Docker images) were added, and the training happens locally in Airflow. Following that, the model gets deployed as a Lambda function. While not ideal, as usually all workloads are supposed to be off-loaded (i.e. with SageMaker, or EC2 / AWS Batch jobs), but easily trained models can still technically be run with the local executor.

The only input the dag has is a `airflow/variables/dataset_spec` secret in `SecretsManager` service, like the following one:

```json
{
    "url": "https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv",
    "name": "iris.data",
    "feature_columns": ["sepal.length", "sepal.width", "petal.length", "petal.width"],
    "target_column": "variety"
}
```

## Prerequisites

* LocalStack
* Docker
* Python 3.8+ / Python Pip
* `make`
* `jq`
* `curl`
* `awslocal`

## Installing

To install the dependencies:

```shell
make install
```

## Starting LocalStack

Make sure that LocalStack is started:

```shell
LOCALSTACK_AUTH_TOKEN=... make start
```

## Running

Run the sample demo script:

```shell
make run
```

## License

This code is available under the Apache 2.0 license.

