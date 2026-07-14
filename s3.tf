resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "model_bucket" {
  bucket = "aws-ml-pipeline-model-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_object" "model_file" {
  bucket = aws_s3_bucket.model_bucket.id
  key    = "spam_model.json"
  source = "spam_model.json"
  etag   = filemd5("spam_model.json")
}