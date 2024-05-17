terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"  # Replace with your preferred region
}

# Lambda Layer
data "archive_file" "lambda_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/build/my-lambda-layer"  # Path to your Python dependencies directory
  output_path = "${path.module}/build/lambda_layer.zip"
}

# Layer bucket
resource "aws_s3_bucket" "lambda_layer_bucket" {
  bucket = "my-lambda-layer-bucket"
}

# Layer ZIP upload
resource "aws_s3_object" "lambda_layer" {
  bucket     = aws_s3_bucket.lambda_layer_bucket.id
  key        = "lambda_layer.zip"
  source     = data.archive_file.lambda_layer_zip.output_path
  depends_on = [data.archive_file.lambda_layer_zip]  # Triggered only if the zip file is created
}

# Lambda Layer from S3
resource "aws_lambda_layer_version" "dependencies" {
  s3_bucket           = aws_s3_bucket.lambda_layer_bucket.id
  s3_key              = aws_s3_object.lambda_layer.key
  layer_name          = "my-lambda-layer"
  compatible_runtimes = ["python3.12"]
  depends_on          = [aws_s3_object.lambda_layer]  # Triggered only if the zip file is uploaded to the bucket
}

# Lambda Function
data "archive_file" "lambda_function" {
  type        = "zip"
  source_file = "${path.module}/src/lambda_function.py"
  output_path = "${path.module}/build/lambda_function.zip"
}

resource "aws_lambda_function" "my_lambda" {
  filename         = data.archive_file.lambda_function.output_path
  function_name    = "my-lambda-function" 
  role             = aws_iam_role.lambda_role.arn  # See IAM Role below
  handler          = "lambda_function.handler" 
  runtime          = "python3.12" 

  layers = [aws_lambda_layer_version.dependencies.arn] 
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_basic_execution"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_logs_policy" {
  name = "lambda_logs_policy"
  role = aws_iam_role.lambda_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}
