# DynamoDB and Kinesis Stream Integration

Simple demo illustrating the integration between DynamoDB and Kinesis streams.

## Prerequisites

- LocalStack
- Docker
- `make`
- Python >= 3.7
- `tflocal`


## Running

Make sure that LocalStack is started:

```
DEBUG=1 localstack start
```

Deploy the app with Terraform:

```
tflocal init
tflocal apply --auto-approve
```

You can now start the Python script that subscribes to the Kinesis shard, listen, and prints to the changes happening in the DynamoDB table:

```
pip install boto3
python test_stream_consumer.py
```

You can now populate the DynamoDB table with:

```
./ddb-data.sh
```

The Python script will start printing the records the shards receive to the console.

