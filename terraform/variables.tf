variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "blacklist"
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
  default     = 5000
}

# Database variables
variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "PostgreSQL master password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "blacklist_db"
}

# Application secrets
variable "secret_key" {
  description = "Flask SECRET_KEY"
  type        = string
  sensitive   = true
}

variable "jwt_secret_key" {
  description = "JWT secret key"
  type        = string
  sensitive   = true
}

variable "static_token" {
  description = "Static Bearer token for API authentication"
  type        = string
  sensitive   = true
}

variable "new_relic_license_key" {
  description = "New Relic License Key (INGEST)"
  type        = string
  sensitive   = true
}
