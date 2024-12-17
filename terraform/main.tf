provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "fc-transformer-rg"
  location = "East US"
}

resource "azurerm_storage_account" "main" {
  name                     = "fctransformer"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "videos" {
  name                  = "videos"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "audios" {
  name                  = "audios"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_sql_server" "main" {
  name                         = "fctransformer-sql-server"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.AZURE_SQL_ADMIN
  administrator_login_password = var.AZURE_SQL_PASSWORD
}

resource "azurerm_sql_database" "main" {
  name                = "fctransformer-prompt-db"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  server_name         = azurerm_sql_server.main.name
  sku_name            = "Basic"
}

resource "azurerm_app_service_plan" "main" {
  name                = "fc-transformer-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_function_app" "main" {
  name                       = "fc-transformer-function"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  app_service_plan_id        = azurerm_app_service_plan.main.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"  # Change to Python runtime
    PYTHON_VERSION           = "3.9"     # Specify Python version (e.g., 3.8, 3.9)
    AzureWebJobsStorage      = azurerm_storage_account.main.primary_blob_connection_string
    SqlDatabaseConnection    = azurerm_sql_database.main.id
    RUNWAYML_API_KEY         = var.RUNWAYML_API_KEY
    YOUTUBE_CLIENT_ID        = var.YOUTUBE_CLIENT_ID
    YOUTUBE_CLIENT_SECRET    = var.YOUTUBE_CLIENT_SECRET
    YOUTUBE_REFRESH_TOKEN    = var.YOUTUBE_REFRESH_TOKEN
  }
}
