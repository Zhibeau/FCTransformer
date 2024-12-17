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

resource "azurerm_postgresql_server" "main" {
  name                = "fctransformer-postgres-server"  # Replace with your server name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  administrator_login          = var.AZURE_SQL_ADMIN
  administrator_login_password = var.AZURE_SQL_PASSWORD
  version             = "11"                            # PostgreSQL version

  # Required arguments
  sku_name                = "B_Gen5_1"                  # Pricing tier
  ssl_enforcement_enabled = true                       # Enforce SSL

  storage_mb       = 5120                              # Storage in MB (e.g., 5GB)
  backup_retention_days = 7                            # Retention period for backups
  geo_redundant_backup_enabled = false                 # Geo-redundancy

  tags = {
    environment = "production"
  }
}

resource "azurerm_postgresql_database" "main" {
  name                = "fctransformer-prompt-db"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_postgresql_server.main.name

  charset   = "UTF8"          # Required: Character set for the database
  collation = "English_United States.1252"  # Required: Collation for the database
}

resource "azurerm_service_plan" "main" {
  name                = "fc-transformer-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  os_type  = "Linux"          # Required: Specify "Linux" or "Windows" based on your app
  sku_name = "Y1"             # Required: Pricing tier (e.g., Y1 for consumption plan)
}

resource "azurerm_linux_function_app" "main" {
  name                = "fc-transformer-function"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9"  # Specify the Python runtime version
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"  # Runtime type: Python
    AzureWebJobsStorage      = azurerm_storage_account.main.primary_blob_connection_string
    SqlDatabaseConnection    = azurerm_postgresql_server.main.fqdn
    RUNWAYML_API_KEY         = var.RUNWAYML_API_KEY
    YOUTUBE_CLIENT_ID        = var.YOUTUBE_CLIENT_ID
    YOUTUBE_CLIENT_SECRET    = var.YOUTUBE_CLIENT_SECRET
    YOUTUBE_REFRESH_TOKEN    = var.YOUTUBE_REFRESH_TOKEN
  }
}

