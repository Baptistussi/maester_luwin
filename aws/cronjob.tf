resource "aws_ssm_parameter" "private_key" {
  name        = "/starkbank/private-key"
  description = "Starkbank private key for invoice processing"
  type        = "SecureString"
  value       = file("${path.module}/../keys/privateKey.pem")
}

resource "aws_iam_role" "cronjob_lambda_role" {
  name = "cronjob-lambda-role"

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

resource "aws_iam_role_policy" "cronjob_lambda_policy" {
  name = "cronjob-lambda-policy"
  role = aws_iam_role.cronjob_lambda_role.id

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

resource "aws_lambda_function" "cronjob" {
  filename         = "../dist/cronjob.zip"
  function_name    = "starkbank-cronjob"
  role             = aws_iam_role.cronjob_lambda_role.arn
  handler          = "cronjob.add_invoices.lambda_handler"
  source_code_hash = filebase64sha256("../dist/cronjob.zip")
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

resource "aws_scheduler_schedule" "cronjob_schedule" {
  name        = "starkbank-cronjob-schedule"
  description = "Schedule for starkbank cronjob"
  state       = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = var.cron_schedule

  target {
    arn      = aws_lambda_function.cronjob.arn
    role_arn = aws_iam_role.eventbridge_scheduler_role.arn
  }
}

resource "aws_iam_role" "eventbridge_scheduler_role" {
  name = "eventbridge-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_scheduler_policy" {
  name = "eventbridge-scheduler-policy"
  role = aws_iam_role.eventbridge_scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = aws_lambda_function.cronjob.arn
      }
    ]
  })
}
