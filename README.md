# VMSM
repositorio de volume and merchandise management system

## pasos basicos para correr la aplicación

1. tener python 3
3. tener el intalador de paquete de python (PIP)
4. tener el paquete de "virtualenv", en caso de no tenerlo correr el comando `pip install virtualenv`
5. hacer un entorno virtual `virtualenv -p python env` en la carpeta del proyecto (VMSM)
6. entrar al entorno virtual `.\env\Scripts\activate`
7. instalar todas las dependecias del proyecto `pip install -r requirements.txt`
8. puedes revisar la versión de django con `python -m django --version`
9. Para hacer las migraciones, Primero cambiar las variables de entorno en un .env tomando como referencia el .env.sample, despues ejecurar los siguientes comandos:
    1. `python .\project\manage.py  makemigrations` 
    2. `python .\project\manage.py migrate appLogin 0002`
    3. `python .\project\manage.py migrate`
    4. (Opcional) Crear un super usuario con django `python .\project\manage.py createsuperuser` poner nombre de usuario,mail y dos veces contraseña.
10. Para levantar el servidor entrar en la carpeta "project" `python .\project\manage.py runserver`
