# deploy_to_azure.ps1
# Script de PowerShell para desplegar la aplicación a Azure App Service

# Configuración - Modificar estos valores
$RESOURCE_GROUP = "huerta-app-rg-1"
$APP_SERVICE_PLAN = "plan-rag-api-basico"
$APP_NAME = "huerta-query-1"
# Lista de regiones a probar en orden
$LOCATIONS = @("westus", "westus2", "eastus2", "centralus", "northeurope", "westeurope", "southeastasia", "japaneast")
# Lista de SKUs a probar
$SKUS = @("F1", "B1", "B2")  # F1 es gratis pero con limitaciones, B1 es el más económico con todas las funciones

# Variables de entorno para la aplicación
$OPENAI_API_KEY = "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"

Write-Host "Preparando la aplicación para deployment..." -ForegroundColor Yellow

# 1. Verifica que tienes Azure CLI instalado
try {
    $azVersion = az --version
    Write-Host "Azure CLI está instalado" -ForegroundColor Green
} catch {
    Write-Host "Azure CLI no está instalado. Por favor instálalo primero." -ForegroundColor Red
    Write-Host "Visita: https://docs.microsoft.com/es-es/cli/azure/install-azure-cli-windows"
    exit 1
}

# 2. Comprime la base de datos Chroma (si existe)
if (Test-Path -Path "chroma_db") {
    Write-Host "Comprimiendo la carpeta chroma_db..."
    Compress-Archive -Path "chroma_db" -DestinationPath "chroma_db.zip" -Force
} else {
    Write-Host "No se encontró la carpeta chroma_db. Asegúrate de tenerla antes de desplegar." -ForegroundColor Yellow
    $CONTINUE = Read-Host "¿Continuar de todos modos? (s/n)"
    if ($CONTINUE -ne "s") {
        exit 1
    }
}

# 3. Login a Azure (si no estás ya autenticado)
Write-Host "Iniciando sesión en Azure..."
az account show > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    az login
}

# 4. Intentar crear un grupo de recursos con diferentes ubicaciones
$resourceCreated = $false
$successLocation = ""
$successSku = ""

foreach ($location in $LOCATIONS) {
    Write-Host "Probando con la ubicación: $location" -ForegroundColor Yellow
    
    # Intentar crear el grupo de recursos
    Write-Host "Creando grupo de recursos en $location..."
    az group create --name $RESOURCE_GROUP --location $location > $null 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Grupo de recursos creado con éxito en $location" -ForegroundColor Green
        $successLocation = $location
        
        # Probar con diferentes SKUs
        foreach ($sku in $SKUS) {
            Write-Host "Probando con SKU: $sku"
            
            # Intentar crear el plan de App Service
            Write-Host "Creando plan de App Service con SKU $sku en $location..."
            az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku $sku --is-linux > $null 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Plan de App Service creado con éxito con SKU $sku en $location" -ForegroundColor Green
                $successSku = $sku
                $resourceCreated = $true
                break
            } else {
                Write-Host "No se pudo crear el plan de App Service con SKU $sku en $location. Probando con otro SKU..." -ForegroundColor Yellow
            }
        }
        
        # Si se creó el plan, salir del bucle de ubicaciones
        if ($resourceCreated) {
            break
        } else {
            # Si no se pudo crear el plan con ningún SKU, eliminar el grupo de recursos
            Write-Host "No se pudo crear el plan de App Service en $location con ningún SKU. Eliminando grupo de recursos..." -ForegroundColor Yellow
            az group delete --name $RESOURCE_GROUP --yes --no-wait
        }
    } else {
        Write-Host "No se pudo crear el grupo de recursos en $location. Probando con otra ubicación..." -ForegroundColor Yellow
    }
}

# Verificar si se pudo crear el recurso
if (-not $resourceCreated) {
    Write-Host "No se pudo crear el recurso en ninguna ubicación con ningún SKU. Por favor, verifica tu suscripción." -ForegroundColor Red
    exit 1
}

# Mostrar información de éxito
Write-Host "Recursos creados con éxito en la ubicación $successLocation con SKU $successSku" -ForegroundColor Green

# 5. Crear App de Azure
Write-Host "Creando App Service..."
az webapp create --name $APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "PYTHON:3.9"

# 6. Configurar variables de entorno
Write-Host "Configurando variables de entorno..."
az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings OPENAI_API_KEY=$OPENAI_API_KEY SCM_DO_BUILD_DURING_DEPLOYMENT=true WEBSITE_RUN_FROM_PACKAGE=0

# 7. Configurar el script de inicio
Write-Host "Configurando script de inicio..."
az webapp config set --name $APP_NAME --resource-group $RESOURCE_GROUP --startup-file "startup.sh"

# 8. Habilitar registro de aplicación
Write-Host "Habilitando registros..."
az webapp log config --name $APP_NAME --resource-group $RESOURCE_GROUP --docker-container-logging filesystem

# 9. Desplegar los archivos usando ZIP deployment
Write-Host "Desplegando la aplicación..."
# Crear un paquete ZIP con todos los archivos necesarios
Compress-Archive -Path @("query.py", "requirements.txt", "Procfile", "startup.sh", ".deployment", "chroma_db.zip") -DestinationPath "deployment.zip" -Force

# Subir el ZIP a Azure
az webapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $APP_NAME --src "deployment.zip"

# 10. Mostrar la URL de la aplicación
$URL = az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv
Write-Host "Despliegue completado!" -ForegroundColor Green
Write-Host "Tu aplicación está disponible en: https://$URL" -ForegroundColor Green
Write-Host "Puedes ver los logs con:"
Write-Host "  az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"

# Limpieza
Write-Host "Limpiando archivos temporales..."
Remove-Item -Path "deployment.zip" -Force