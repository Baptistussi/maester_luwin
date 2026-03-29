variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_id" {
  description = "Starkbank project ID"
  type        = string
  sensitive   = true
}

variable "cron_schedule" {
  description = "Cron expression for the schedule (UTC)"
  type        = string
  default     = "rate(3 hours)"
}
