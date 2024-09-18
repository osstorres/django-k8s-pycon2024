output "ecr_repository_urls" {
  description = "List of ECR repository URLs."
  value       = aws_ecr_repository.repositories[*].repository_url
}