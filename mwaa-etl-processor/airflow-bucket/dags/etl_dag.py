from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@dag(schedule_interval=None, start_date=days_ago(1), tags=['example'])
def example_s3_list_dag():

    @task
    def list_environment_variables():
        import os
        for key, value in os.environ.items():
            print(f"Found env var: {key}={value}")
        return dict(os.environ.items())

    @task
    def list_s3_bucket(env_items):
        hook = S3Hook(aws_conn_id='aws_default')
        bucket_name = 'airflow'  # Replace with your S3 bucket name
        keys = hook.list_keys(bucket_name)
        for key in keys:
            print(f"Found key: {key}")
        return keys

    list_s3_bucket(list_environment_variables())

dag = example_s3_list_dag()
