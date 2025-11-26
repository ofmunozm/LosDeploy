# SSM Parameters para secrets/variables de entorno

# DATABASE_URL construido dinámicamente
resource "aws_ssm_parameter" "database_url" {
  name        = "/${var.project_name}/database_url"
  description = "PostgreSQL connection string"
  type        = "SecureString"
  value       = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.main.address}:5432/${var.db_name}"

  tags = {
    Name = "${var.project_name}-database-url"
  }
}

# Flask SECRET_KEY
resource "aws_ssm_parameter" "secret_key" {
  name        = "/${var.project_name}/secret_key"
  description = "Flask SECRET_KEY"
  type        = "SecureString"
  value       = var.secret_key

  tags = {
    Name = "${var.project_name}-secret-key"
  }
}

# JWT Secret Key
resource "aws_ssm_parameter" "jwt_secret_key" {
  name        = "/${var.project_name}/jwt_secret_key"
  description = "JWT secret key"
  type        = "SecureString"
  value       = var.jwt_secret_key

  tags = {
    Name = "${var.project_name}-jwt-secret-key"
  }
}

# Static Bearer Token
resource "aws_ssm_parameter" "static_token" {
  name        = "/${var.project_name}/static_token"
  description = "Static Bearer token for API authentication"
  type        = "SecureString"
  value       = var.static_token

  tags = {
    Name = "${var.project_name}-static-token"
  }
}

# New Relic License Key
resource "aws_ssm_parameter" "new_relic_license_key" {
  name        = "/${var.project_name}/new_relic_license_key"
  description = "New Relic License Key para APM"
  type        = "SecureString"
  value       = var.new_relic_license_key

  tags = {
    Name = "${var.project_name}-new-relic-license"
  }
}
