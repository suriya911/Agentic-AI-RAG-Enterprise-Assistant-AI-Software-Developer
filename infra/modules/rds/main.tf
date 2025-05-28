resource "aws_security_group" "rds" {
  name        = "rag-assistant-rds-sg"
  description = "Security group for RDS instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.eks_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rag-assistant-rds-sg"
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "rag-assistant-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "rag-assistant-db-subnet-group"
  }
}

resource "aws_db_instance" "main" {
  identifier           = var.identifier
  engine              = "postgres"
  engine_version      = var.engine_version
  instance_class      = var.instance_class
  allocated_storage   = var.allocated_storage
  storage_type        = "gp2"
  db_name             = var.db_name
  username            = var.username
  password            = var.password
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  tags = {
    Name = "rag-assistant-db"
  }
} 