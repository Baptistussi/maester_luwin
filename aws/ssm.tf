resource "aws_ssm_parameter" "private_key" {
  name        = "/starkbank/private-key"
  description = "Starkbank private key for invoice processing"
  type        = "SecureString"
  value       = file("${path.module}/../keys/privateKey.pem")
}
