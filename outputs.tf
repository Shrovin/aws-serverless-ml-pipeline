output "api_endpoint" {
  value = "${aws_apigatewayv2_stage.default_stage.invoke_url}predict"
}