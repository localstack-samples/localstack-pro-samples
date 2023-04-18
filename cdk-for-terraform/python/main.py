from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws.provider import AwsProvider
from imports.aws.sns_topic import SnsTopic
from imports.aws.dynamodb_table import DynamodbTable
from imports.terraform_aws_modules.aws import Vpc
from localstack_config import AWS_CONFIG


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, "Aws", **AWS_CONFIG)

        Vpc(
            self,
            "CustomVpc",
            name="custom-vpc",
            cidr="10.0.0.0/16",
            azs=["us-east-1a", "us-east-1b"],
            public_subnets=["10.0.1.0/24", "10.0.2.0/24"],
        )

        SnsTopic(self, "Topic", display_name="my-first-sns-topic")

        DynamodbTable(
            self,
            "DynamoDB",
            name="my-dynamodb-table",
            read_capacity=1,
            write_capacity=1,
            hash_key="Id",
            attribute=[
                {"name": "Id", "type": "S"},
            ],
        )


app = App()
MyStack(app, "python-aws")

app.synth()
