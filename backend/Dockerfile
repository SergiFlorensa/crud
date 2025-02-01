# Usa una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y otras librerías de Python
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  # Limpiar la caché de apt para reducir el tamaño de la imagen

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instalar email-validator necesario para la validación de correos electrónicos
RUN pip install pydantic[email]

# Asegurarse de que uvicorn esté instalado
RUN pip install uvicorn

RUN pip install python-multipart

# Exponer el puerto 8000 para la API
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
