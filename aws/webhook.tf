resource "aws_iam_role" "webhook_lambda_role" {
  name = "webhook-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "webhook_lambda_policy" {
  name = "webhook-lambda-policy"
  role = aws_iam_role.webhook_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter"
        ]
        Resource = "arn:aws:ssm:*:*:parameter/starkbank/*"
      }
    ]
  })
}

resource "aws_lambda_function" "webhook" {
  filename         = "../dist/lambda.zip"
  function_name    = "starkbank-webhook"
  role             = aws_iam_role.webhook_lambda_role.arn
  handler          = "src.webhook.webhook.lambda_handler"
  source_code_hash = filebase64sha256("../dist/lambda.zip")
  runtime          = "python3.11"
  timeout          = 60
  memory_size      = 128

  environment {
    variables = {
      ENVIRONMENT    = var.environment
      PROJECT_ID     = var.project_id
      SSM_PARAM_NAME = "/starkbank/private-key"
    }
  }
}

resource "aws_lambda_function_url" "webhook" {
  function_name      = aws_lambda_function.webhook.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["POST"]
    allow_headers     = ["*"]
  }
}
