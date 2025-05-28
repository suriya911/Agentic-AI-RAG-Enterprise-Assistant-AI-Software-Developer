output "log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.main.arn
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.main.name
}

output "cpu_alarm_arn" {
  description = "ARN of the CPU utilization alarm"
  value       = aws_cloudwatch_metric_alarm.cpu_utilization.arn
}

output "memory_alarm_arn" {
  description = "ARN of the memory utilization alarm"
  value       = aws_cloudwatch_metric_alarm.memory_utilization.arn
}

output "db_cpu_alarm_arn" {
  description = "ARN of the database CPU utilization alarm"
  value       = aws_cloudwatch_metric_alarm.db_cpu_utilization.arn
}

output "db_storage_alarm_arn" {
  description = "ARN of the database storage alarm"
  value       = aws_cloudwatch_metric_alarm.db_free_storage.arn
} 