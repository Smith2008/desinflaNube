variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_name" {
  type    = string
  default = "cost-bucket"
}

variable "sns_topic" {
  type    = string
  default = "cost-alerts"
}

variable "lambda_name" {
  type    = string
  default = "cost-pipeline-lambda"
}
