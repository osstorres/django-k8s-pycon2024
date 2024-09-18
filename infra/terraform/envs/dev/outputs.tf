output "db_instance_endpoint" {
  description = "The endpoint of the RDS instance."
  value       = module.network-persistence.db_instance_endpoint
}

# Output del ID de la VPC
output "vpc_id" {
  description = "ID de la VPC"
  value       = module.network-persistence.vpc_id
}

# Outputs de los IDs de las Subnets Privadas
output "private_subnet_1_id" {
  description = "ID de la primera Subnet Privada"
  value       = module.network-persistence.private_subnet_1_id
}

output "private_subnet_2_id" {
  description = "ID de la segunda Subnet Privada"
  value       = module.network-persistence.private_subnet_2_id
}


output "elasticache_cluster_endpoint" {
  description = "Redis endpoint"
  value =  module.network-persistence.elasticache_cluster_endpoint
}

# Outputs de los IDs de las Subnets publicas
output "public_subnet_1_id" {
  description = "ID de la primera Subnet publicas"
  value       = module.network-persistence.public_subnet_1_id
}

output "public_subnet_2_id" {
  description = "ID de la segunda Subnet publicas"
  value       = module.network-persistence.public_subnet_2_id
}


output "security_group_eks_nodes_id" {
  description = "ID security_group_eks_nodes"
  value       = module.network-persistence.security_group_eks_nodes
}

