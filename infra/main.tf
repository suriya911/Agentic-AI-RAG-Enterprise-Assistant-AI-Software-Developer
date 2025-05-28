terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "rag-assistant-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
}

# RDS PostgreSQL
module "rds" {
  source = "./modules/rds"

  identifier        = var.db_identifier
  engine_version    = var.db_engine_version
  instance_class    = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  db_name          = var.db_name
  username         = var.db_username
  password         = var.db_password
  vpc_id           = module.vpc.vpc_id
  subnet_ids       = module.vpc.private_subnet_ids
}

# S3 Buckets
module "s3" {
  source = "./modules/s3"

  bucket_name = var.documents_bucket_name
}

# Lambda Functions
module "lambda" {
  source = "./modules/lambda"

  function_name = var.lambda_function_name
  runtime      = var.lambda_runtime
  handler      = var.lambda_handler
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
}

# CloudWatch Logs
module "cloudwatch" {
  source = "./modules/cloudwatch"

  log_group_name = var.log_group_name
  retention_days = var.log_retention_days
} 