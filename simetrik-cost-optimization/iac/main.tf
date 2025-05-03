provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "cost_bucket" {
  bucket = var.bucket_name
}

resource "aws_sns_topic" "cost_alerts" {
  name = var.sns_topic
}

resource "aws_lambda_function" "cost_pipeline" {
  function_name = var.lambda_name
  handler       = "lambda_function.handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "../deployment/lambda_package.zip"
  environment {
    variables = {
      BUCKET_NAME   = aws_s3_bucket.cost_bucket.id
      SNS_TOPIC_ARN = aws_sns_topic.cost_alerts.arn
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.lambda_policy.json
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "s3:PutObject",
      "sns:Publish",
      "ce:GetCostAndUsage"
    ]
    resources = ["*"]
  }
}
