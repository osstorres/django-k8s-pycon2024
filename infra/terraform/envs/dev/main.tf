module "network-persistence" {
  source = "../../modules/network-persistence"
  # RDS
  db_instance_identifier = "dev-db-instance"
  db_instance_class      = "db.t3.micro"
  engine_version         = "15.4"
  username               = "core"
  password               = "changemepassword"
  db_name                = "dev_db"
  # REDIS
  cluster_id         = "dev-redis-cluster"
  node_type          = "cache.t4g.micro"
  num_cache_nodes    = 1
}

module "ecr" {
  source = "../../modules/ecr"
  repository_names = ["core-application", "analytics-application"]
}

module "secrets" {
  source = "../../modules/secrets"

}