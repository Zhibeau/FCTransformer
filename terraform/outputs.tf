output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "sql_server_name" {
  value = azurerm_postgresql_server.main.name
}

output "function_app_name" {
  value = azurerm_linux_function_app.main.name  # Updated to match the correct resource
}
