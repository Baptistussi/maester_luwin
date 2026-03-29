variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "cron_schedule" {
  description = "Cron expression for the schedule (UTC)"
  type        = string
  default     = "rate(3 hours)"
}
