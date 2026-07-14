resource "aws_dynamodb_table" "predictions" {
  name         = "ml-pipeline-predictions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "request_id"

  attribute {
    name = "request_id"
    type = "S"
  }
}