import json
import os
import boto3

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

MODEL_BUCKET = os.environ["MODEL_BUCKET"]
MODEL_KEY = os.environ["MODEL_KEY"]
TABLE_NAME = os.environ["TABLE_NAME"]

_model_cache = None

def load_model():
    global _model_cache
    if _model_cache is None:
        obj = s3.get_object(Bucket=MODEL_BUCKET, Key=MODEL_KEY)
        _model_cache = json.loads(obj["Body"].read())
    return _model_cache

def predict(text, model):
    vocab = model["vocabulary"]
    classes = model["classes"]
    log_prior = model["class_log_prior"]
    log_prob = model["feature_log_prob"]

    words = text.lower().split()
    scores = list(log_prior)
    for word in words:
        if word in vocab:
            idx = vocab[word]
            for c in range(len(classes)):
                scores[c] += log_prob[c][idx]

    best_idx = scores.index(max(scores))
    return classes[best_idx]

def handler(event, context):
    model = load_model()

    body = json.loads(event.get("body") or "{}")
    text = body.get("text", "")

    if not text:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'text' field in request body"})
        }

    prediction = predict(text, model)
    request_id = context.aws_request_id

    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        "request_id": request_id,
        "text": text,
        "prediction": prediction,
    })

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"prediction": prediction, "request_id": request_id})
    }