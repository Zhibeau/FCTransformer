variable "location" {
  default = "East US"
}

variable "resource_group_name" {
  default = "fc-transformer-rg"
}

variable "sql_admin_username" {
  description = "The SQL Server admin username"
  type        = string
}

variable "sql_admin_password" {
  description = "The SQL Server admin password"
  type        = string
  sensitive   = true
}

variable "youtube_api_key" {
  description = "YouTube API Key for video publishing"
  type        = string
  sensitive   = true
}
