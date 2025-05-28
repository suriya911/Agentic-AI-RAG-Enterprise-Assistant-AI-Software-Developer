variable "log_group_name" {
  description = "Name of the CloudWatch log group"
  type        = string
}

variable "retention_days" {
  description = "Number of days to retain logs"
  type        = number
}

variable "cluster_name" {
  description = "Name of the ECS cluster"
  type        = string
}

variable "db_instance_id" {
  description = "ID of the RDS instance"
  type        = string
}

variable "sns_topic_arn" {
  description = "ARN of the SNS topic for alarms"
  type        = string
} 