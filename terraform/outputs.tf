output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "sql_server_name" {
  value = azurerm_sql_server.main.name
}

output "function_app_name" {
  value = azurerm_function_app.main.name
}
