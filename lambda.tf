data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function.zip"
}

resource "aws_lambda_function" "predictor" {
  function_name = "ml-pipeline-predictor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.handler"
  runtime       = "python3.12"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      MODEL_BUCKET = aws_s3_bucket.model_bucket.id
      MODEL_KEY    = aws_s3_object.model_file.key
      TABLE_NAME   = aws_dynamodb_table.predictions.name
    }
  }
}