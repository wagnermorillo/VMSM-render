# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer variables de entorno para asegurar que la salida de Python se envíe directamente al terminal sin ser almacenada en búfer
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Crear un directorio para la aplicación
WORKDIR /usr/src/app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Instalar las dependencias
COPY . .

# Exponer el puerto que usa la aplicación (por defecto Express usa el 3000)
EXPOSE 8000

# Comando para ejecutar la aplicación
ENTRYPOINT ["python", "project/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]