resource "aws_db_instance" "core_db" {
  identifier             = var.db_instance_identifier
  instance_class         = var.db_instance_class
  engine                 = "postgres"
  engine_version         = var.engine_version
  username               = var.username
  password               = var.password
  db_name                = var.db_name
  db_subnet_group_name   = aws_db_subnet_group.core_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  allocated_storage      = 20
  publicly_accessible    = false
  skip_final_snapshot     = true

  tags = {
    Name = var.db_name
  }
}


# VPC
resource "aws_vpc" "core_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "core-vpc"
  }
}

# Subnet Private 1
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.core_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"

  tags = {
    Name = "private-subnet-1"
  }
}

# Subnet Private 2
resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.core_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-west-2b"

  tags = {
    Name = "private-subnet-2"
  }
}

# Subnet Public 1
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.core_vpc.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "us-west-2a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
  }
}

# Subnet Public 2
resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.core_vpc.id
  cidr_block              = "10.0.4.0/24"
  availability_zone       = "us-west-2b"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-2"
  }
}

# Associate Route Table with Public Subnets
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}


# ===

# Internet Gateway
resource "aws_internet_gateway" "core_igw" {
  vpc_id = aws_vpc.core_vpc.id

  tags = {
    Name = "core-igw"
  }
}

# Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.core_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.core_igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

# Associate Route Table with Subnets
resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.public.id
}


# =====

# Security Group for EKS Nodes
resource "aws_security_group" "eks_nodes" {
  vpc_id = aws_vpc.core_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "eks-nodes-sg"
  }
}

# Security Group for RDS
resource "aws_security_group" "rds" {
  vpc_id = aws_vpc.core_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_nodes.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-sg"
  }
}


resource "aws_db_subnet_group" "core_subnet_group" {
  name       = "core-rds-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "core-rds-subnet-group"
  }
}


# Security Group for ElastiCache Redis
resource "aws_security_group" "redis_security_group" {
  vpc_id = aws_vpc.core_vpc.id

  ingress {
    from_port       = 11211
    to_port         = 11211
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_nodes.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "redis-sg"
  }
}

# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "core_redis_subnet_group" {
  name       = "core-redis-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "core-redis-subnet-group"
  }
}


# ElastiCache Redis Cluster
resource "aws_elasticache_cluster" "core_redis_cluster" {
  cluster_id           = var.cluster_id
  engine               = "redis"
  node_type            = var.node_type
  num_cache_nodes      = var.num_cache_nodes
  parameter_group_name = "default.redis7"
  subnet_group_name    = aws_elasticache_subnet_group.core_redis_subnet_group.name
  security_group_ids   = [aws_security_group.redis_security_group.id]

  tags = {
    Name = var.cluster_id
  }
}