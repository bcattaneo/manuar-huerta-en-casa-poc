# startup.sh
#!/bin/bash

# Crea la carpeta chroma_db si no existe
mkdir -p chroma_db

# Copia los archivos de la base de datos si se proporcionan como archivos comprimidos
if [ -f "chroma_db.zip" ]; then
  echo "Descomprimiendo base de datos..."
  unzip -o chroma_db.zip -d ./
fi

# Inicia la aplicación con Gunicorn
gunicorn query:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT