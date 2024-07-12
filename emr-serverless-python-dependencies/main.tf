terraform {
  required_version = "~>1.7.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.42.0"
    }
  }
}

provider "aws" {
  region            = "us-east-1"
  s3_use_path_style = true
}

resource "aws_iam_role" "emr-serverless-job-role" {
  assume_role_policy = file("${path.module}/emr-serverless-trust-policy.json")
}

resource "aws_iam_policy" "emr-serverless-job-policy" {
  name   = "EMRServerlessS3AndGlueAccessPolicy"
  policy = templatefile("${path.module}/emr-sample-access-policy.json.tfpl", { bucket = aws_s3_bucket.emr-serverless-job.bucket })
}

resource "aws_iam_role_policy_attachment" "emr-serverless-job-attachment" {
  role       = aws_iam_role.emr-serverless-job-role.name
  policy_arn = aws_iam_policy.emr-serverless-job-policy.arn
}

resource "aws_emrserverless_application" "emr-serverless-application" {
  name          = "emr-serverless"
  release_label = "emr-6.14.0"
  type          = "spark"
}

resource "random_string" "random" {
  length  = 16
  special = false
  upper   = false
}

resource "aws_s3_bucket" "emr-serverless-job" {
  bucket        = "emr-serverless-job-${random_string.random.result}"
  force_destroy = true
}

output "s3_bucket" {
  value = aws_s3_bucket.emr-serverless-job.bucket
}

output "application_id" {
  value = aws_emrserverless_application.emr-serverless-application.id
}

output "role_arn" {
  value = aws_iam_role.emr-serverless-job-role.arn
}
