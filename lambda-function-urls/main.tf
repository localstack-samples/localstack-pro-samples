data "aws_region" "current" {}

resource "aws_lambda_function" "example_lambda" {
  filename         = "function.zip"
  function_name    = "localstack-lamba-url-example"
  role             = "cool-stacklifter"
  handler          = "index.handler"
  source_code_hash = filebase64sha256("function.zip")
  runtime          = "nodejs14.x"
}

resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.example_lambda.arn
  authorization_type = "NONE"
}

output "function_url" {
  description = "Function URL."
  value       = aws_lambda_function_url.lambda_function_url.function_url
}
