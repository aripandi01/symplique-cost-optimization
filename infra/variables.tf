variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "project_prefix" {
  description = "Prefix for resource naming"
  type        = string
}

variable "cosmos_account_name" {
  type = string
}

variable "cosmos_database_name" {
  type = string
}

variable "cosmos_container_name" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "storage_container_name" {
  type = string
}

variable "function_app_name" {
  type = string
}

variable "service_plan_name" {
  type = string
}

