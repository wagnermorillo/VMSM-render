# VMSM
repositorio de volume and merchandise management system

## pasos basicos para correr la aplicación

1. Tener python 3
3. Tener el intalador de paquete de python (PIP)
4. Tener el paquete de "virtualenv", en caso de no tenerlo correr el comando `pip install virtualenv`
5. Hacer un entorno virtual `virtualenv -p python env` o `python -m venv env` en la carpeta del proyecto (VMSM)
6. Entrar al entorno virtual `.\env\Scripts\activate`
7. Descargar las librerias que estan dentro de `Requirements.txt` con el comando `pip install -r .\requirements.txt`
8. Instalar django `pip install django` version 4.2.5
9. (OPCIONAL) Puedes revisar la versión de django con `python -m django --version`
10. Para levantar el servidor entrar en la carpeta "project" `python manage.py runserver`
