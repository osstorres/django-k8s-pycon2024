resource "aws_secretsmanager_secret" "application_secrets" {
  name                           = "application-secrets"
  recovery_window_in_days        = 0
  force_overwrite_replica_secret = true
}

resource "aws_secretsmanager_secret_version" "core_secrets_version" {
  secret_id = aws_secretsmanager_secret.application_secrets.id

  secret_string = jsonencode({
    DJANGO_CONFIGURATION         = "Dev"
    DJANGO_CELERY_BROKER_URL     = "redis://dev-redis-cluster.id.0001.usw2.cache.amazonaws.com:6379/1"
    DJANGO_CELERY_RESULT_BACKEND = "redis://dev-redis-cluster.id.0001.usw2.cache.amazonaws.com:6379/1"
    DATABASE_URL                 = "postgres://core:changemepassword@dev-db-instance.id.us-west-2.rds.amazonaws.com:5432/dev_db"
    CACHE_LOCATION               = "redis://dev-redis-cluster.id.0001.usw2.cache.amazonaws.com:6379/2"
  })
}

# Policy allowing access to the secret
resource "aws_iam_policy" "secrets_manager_policy" {
  name = "EKSSecretsManagerPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
        Resource = aws_secretsmanager_secret.application_secrets.arn
      }
    ]
  })
}
