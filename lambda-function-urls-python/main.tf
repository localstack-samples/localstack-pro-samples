resource "aws_lambda_function" "trending" {
  filename         = "function.zip"
  function_name    = "trending"
  role             = "cool-stacklifter"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("function.zip")
  runtime          = "python3.9"
}

resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.trending.arn
  authorization_type = "NONE"
}

output "function_url" {
  description = "Function URL."
  value       = aws_lambda_function_url.lambda_function_url.function_url
}
