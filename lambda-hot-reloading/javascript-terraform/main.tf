terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "test_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  function_name = "hotreloadlambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.handler"

  s3_bucket = "hot-reload"
  s3_key    = "${abspath(path.root)}/lambda_src"

  runtime = "nodejs16.x"

  environment {
    variables = {
      foo = "bar"
    }
  }
}

output "hot_reloading_lambda_arn" {
  value = aws_lambda_function.test_lambda.arn
}