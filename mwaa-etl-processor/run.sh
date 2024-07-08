#!/bin/bash
set -euxo pipefail

AIRFLOW_CONFIG=$(cat <<EOF | jq -c .
{
  "core.dags_are_paused_at_creation": "False",
  "scheduler.min_file_process_interval": "0",
  "scheduler.dag_dir_list_interval": "10",
  "secrets.backend": "airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend",
  "secrets.backend_kwargs": "{\"connections_prefix\": \"airflow/connections/\", \"variables_prefix\": \"airflow/variables/\", \"endpoint_url\": \"https://localhost.localstack.cloud:4566\", \"aws_access_key_id\": \"test\", \"aws_secret_access_key\": \"test\", \"region_name\": \"us-east-1\"}"
}
EOF
)

DATASET_CONFIG=$(cat <<EOF | jq -c .
{
    "url": "https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv",
    "name": "iris.data",
    "feature_columns": ["sepal.length", "sepal.width", "petal.length", "petal.width"],
    "target_column": "variety"
}
EOF
)

# Create default AWS connection for MWAA environment
awslocal secretsmanager create-secret \
    --name airflow/connections/aws_default \
    --secret-string '{"conn_type": "aws", "login": "test", "password": "test", "extra": {"region_name": "us-east-1", "endpoint_url": "https://localhost.localstack.cloud:4566"}}'

# Create variable that holds the URL to the Iris dataset
awslocal secretsmanager create-secret \
    --name airflow/variables/dataset_spec \
    --secret-string "$DATASET_CONFIG"

# Create MWAA environment with default AWS connection
awslocal s3 mb s3://airflow
awslocal mwaa create-environment \
    --name my-mwaa-env \
    --airflow-version 2.8.1 \
    --dag-s3-path /dags \
    --airflow-configuration-options "$AIRFLOW_CONFIG" \
    --execution-role-arn arn:aws:iam::000000000000:role/airflow-role \
    --source-bucket-arn arn:aws:s3:::airflow \
    --network-configuration {} \
    --endpoint-url http://localhost.localstack.cloud:4566

# Upload DAG to MWAA environment
awslocal s3 cp --recursive airflow-bucket s3://airflow
