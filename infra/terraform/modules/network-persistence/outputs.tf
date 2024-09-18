output "db_instance_endpoint" {
  description = "The endpoint of the RDS instance."
  value       = aws_db_instance.core_db.endpoint
}

# Output del ID de la VPC
output "vpc_id" {
  description = "ID de la VPC"
  value       = aws_vpc.core_vpc.id
}

# Outputs de los IDs de las Subnets Privadas
output "private_subnet_1_id" {
  description = "ID de la primera Subnet Privada"
  value       = aws_subnet.private_1.id
}

output "private_subnet_2_id" {
  description = "ID de la segunda Subnet Privada"
  value       = aws_subnet.private_2.id
}


output "public_subnet_1_id" {
  value = aws_subnet.public_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_2.id
}

output "elasticache_cluster_endpoint" {
  value = aws_elasticache_cluster.core_redis_cluster.cache_nodes
}

output "security_group_eks_nodes" {
  value = aws_security_group.eks_nodes.id
}