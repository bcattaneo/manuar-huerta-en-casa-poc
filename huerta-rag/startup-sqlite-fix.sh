#!/bin/bash

# startup-sqlite-fix.sh
# Script de inicio que instala una versión actualizada de SQLite antes de iniciar la aplicación

echo "Iniciando script de arranque personalizado..."

# Crear la carpeta chroma_db si no existe
mkdir -p chroma_db

# Descomprimir la base de datos si existe
if [ -f "chroma_db.zip" ]; then
  echo "Descomprimiendo base de datos..."
  unzip -o chroma_db.zip -d ./
  echo "Base de datos descomprimida"
fi

# Verificar la versión actual de SQLite
SQLITE_VERSION=$(sqlite3 --version)
echo "Versión actual de SQLite: $SQLITE_VERSION"

# Instalación de una versión más reciente de SQLite3
echo "Instalando dependencias para compilar SQLite..."
apt-get update
apt-get install -y wget build-essential tcl

# Descargar SQLite más reciente
echo "Descargando SQLite 3.42.0..."
wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz
tar -xzf sqlite-autoconf-3420000.tar.gz
cd sqlite-autoconf-3420000

# Compilar e instalar SQLite
echo "Compilando e instalando SQLite..."
./configure
make
make install

# Actualizar la configuración de las bibliotecas compartidas
echo "Actualizando configuración de bibliotecas..."
ldconfig

# Verificar la nueva versión
cd ..
SQLITE_VERSION_NEW=$(sqlite3 --version)
echo "Nueva versión de SQLite: $SQLITE_VERSION_NEW"

# Continuar con el inicio normal de la aplicación
echo "Iniciando la aplicación con Gunicorn..."
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
gunicorn query:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT