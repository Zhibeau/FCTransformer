provider "azurerm" {
  features {}

  subscription_id = var.AZURE_SUBSCRIPTION_ID
  client_id       = var.AZURE_CLIENT_ID
  client_secret   = var.AZURE_CLIENT_SECRET
  tenant_id       = var.ARM_TENANT_ID
  resource_provider_registrations = "none"
}

resource "azurerm_resource_group" "main" {
  name     = "fc-transformer-rg"
  location = "Canada East"
}

resource "azurerm_storage_account" "main" {
  name                     = "fctransformer"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  depends_on = [azurerm_resource_group.main]
}

resource "azurerm_storage_container" "videos" {
  name                  = "videos"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
  depends_on = [azurerm_storage_account.main]
}

resource "azurerm_storage_container" "audios" {
  name                  = "audios"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
  depends_on = [azurerm_storage_account.main]
}


resource "azurerm_service_plan" "main" {
  name                = "fc-transformer-flex-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "main" {
  name                = "fc-transformer-function"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  depends_on = [azurerm_service_plan.main]

  site_config {
    application_stack {
      python_version = "3.11"  # Specify the Python runtime version
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"  # Runtime type: Python
    AzureWebJobsStorage      = azurerm_storage_account.main.primary_blob_connection_string
    RUNWAYML_API_KEY         = var.RUNWAYML_API_KEY
    YOUTUBE_CLIENT_ID        = var.YOUTUBE_CLIENT_ID
    YOUTUBE_CLIENT_SECRET    = var.YOUTUBE_CLIENT_SECRET
    YOUTUBE_REFRESH_TOKEN    = var.YOUTUBE_REFRESH_TOKEN
  }
}

