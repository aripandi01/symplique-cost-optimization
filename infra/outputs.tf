output "cosmos_endpoint" {
  value = azurerm_cosmosdb_account.cosmos.endpoint
}

output "blob_connection_string" {
  value = azurerm_storage_account.blob.primary_connection_string
  sensitive = true
}

