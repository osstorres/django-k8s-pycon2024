variable "db_instance_identifier" {
  description = "The DB Instance Identifier."
  type        = string
}

variable "db_instance_class" {
  description = "The database instance class."
  type        = string
  default     = "db.t3.medium"
}

variable "engine_version" {
  description = "The PostgreSQL engine version."
  type        = string
  default     = "13.7"
}

variable "username" {
  description = "The master username for the database."
  type        = string
}

variable "password" {
  description = "The master user password for the database."
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "The name of the database."
  type        = string
}


variable "cluster_id" {
  description = "The ID of the Redis cluster."
  type        = string
}

variable "node_type" {
  description = "The instance class used for the Redis cluster."
  type        = string
  default     = "cache.t3.medium"
}

variable "num_cache_nodes" {
  description = "The number of cache nodes in the Redis cluster."
  type        = number
  default     = 1
}

