data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "ml-pipeline-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_permissions" {
  statement {
    sid       = "ReadModelFromS3"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.model_bucket.arn}/${aws_s3_object.model_file.key}"]
  }

  statement {
    sid       = "WriteToDynamoDB"
    actions   = ["dynamodb:PutItem"]
    resources = [aws_dynamodb_table.predictions.arn]
  }

  statement {
    sid = "WriteLogs"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role_policy" "lambda_permissions" {
  name   = "ml-pipeline-lambda-permissions"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_permissions.json
}