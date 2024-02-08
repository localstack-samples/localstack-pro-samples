import boto3
import time


endpoint_url = "http://localhost.localstack.cloud:4566"
stream_name = "demo_stream"


kinesis_client = boto3.client(
    "kinesis",
    endpoint_url=endpoint_url,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

response = kinesis_client.describe_stream(
    StreamName=stream_name,
)
stream_arn = response["StreamDescription"]["StreamARN"]
shard_id = response["StreamDescription"]["Shards"][0]["ShardId"]

consumer_name = "ls_consumer"
response = kinesis_client.register_stream_consumer(
    StreamARN=stream_arn, ConsumerName=consumer_name
)

consumer_arn = response["Consumer"]["ConsumerARN"]

response = kinesis_client.subscribe_to_shard(
    ConsumerARN=consumer_arn,
    ShardId=shard_id,
    StartingPosition={"Type": "TRIM_HORIZON"},
)

try:
    for record in response["EventStream"]:
        print("****************")
        print(record)
except Exception as e:
    print(f"Error reading stream: {str(e)}")
