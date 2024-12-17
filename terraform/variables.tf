variable "location" {
  default = "East US"
}

variable "resource_group_name" {
  default = "fc-transformer-rg"
}

variable "AZURE_CLIENT_ID" {
  description = "Azure client id"
  type        = string
  sensitive   = true
}

variable "ARM_TENANT_ID" {
  description = "Azure tenant id"
  type        = string
  sensitive   = true
}

variable "AZURE_SUBSCRIPTION_ID" {
  description = "Azure subscription id"
  type        = string
  sensitive   = true
}

variable "AZURE_CLIENT_SECRET" {
  description = "Azure client secret"
  type        = string
  sensitive   = true
}

variable "AZURE_SQL_ADMIN" {
  description = "The SQL Server admin username"
  type        = string
}

variable "AZURE_SQL_PASSWORD" {
  description = "The SQL Server admin password"
  type        = string
  sensitive   = true
}

variable "RUNWAYML_API_KEY" {
  description = "RunawayML API key for video generation"
  type        = string
  sensitive   = true
}

variable "YOUTUBE_CLIENT_ID" {
  description = "Youtube client ID"
  type        = string
  sensitive   = true
}

variable "YOUTUBE_CLIENT_SECRET" {
  description = "Youtube client secret"
  type        = string
  sensitive   = true
}

variable "YOUTUBE_REFRESH_TOKEN" {
  description = "Youtube refresh token"
  type        = string
  sensitive   = true
}