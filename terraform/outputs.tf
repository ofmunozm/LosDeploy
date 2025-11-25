output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer (URL pública del API)"
  value       = aws_lb.main.dns_name
}

output "alb_url" {
  description = "Full URL of the API"
  value       = "http://${aws_lb.main.dns_name}"
}

output "ecr_repository_url" {
  description = "ECR repository URL for docker push"
  value       = aws_ecr_repository.main.repository_url
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.main.endpoint
}

output "rds_address" {
  description = "RDS PostgreSQL address (sin puerto)"
  value       = aws_db_instance.main.address
}

output "ecs_cluster_name" {
  description = "ECS Cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS Service name"
  value       = aws_ecs_service.main.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch Log Group for ECS tasks"
  value       = aws_cloudwatch_log_group.ecs.name
}
