# Mac_Mail

Sistema de gestión de envío de correos a clientes.



Puede descargar docker desde el siguiente link: [docker-desktop](https://www.docker.com/products/docker-desktop/)

[TOC]

## Comandos para la ejecución en desarrollo

Activar las variables de ambiente en python

```bash
source app/env/Scripts/activate
```

Para correr el proyecto ejecute el comando

```bash
 docker-compose -f docker-compose.yml up -d 
```

## Accesos

## Sobre los directorios

En el proyecto se encuentran los siguientes directorios

- app: Incluye todos los archivos para el funcionamiento de la api rest 

## Sobre el desarrollo

## Comandos utiles Docker

```bash
docker build -t api_image .
docker run -d --name api_docker -p 80:80 api_image
```

### Base de datos

```bash
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

Acceder por consola

```bash
docker ps
docker exec -i -t d83c525a65b3  /bin/bash
```

### Consideraciones a tener en cuenta

## To create a super User

python manage.py createsuperuser

iberlot
Julia3134!

## Comandos para la creación de ambiente en la nube

```bash
sudo apt-get update && apt-get -y dist-upgrade
sudo apt-get install git
sudo apt-get install python3 python3-dev default-libmysqlclient-dev build-essential
pip install --upgrade pip
sudo apt install pkgconf
export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`

cd cd /home/MacMalling_usr/.local/lib/python3.8/site-packages/django/contrib/admin/static/admin/js/admin/
ln -s ~/MacMailing/app/static_files/admin/js/admin/admin_script.js admin_script.js

ssh -i keys/MacMallingAppPc_key.pem MacMalling_usr@macmailling.eastus.cloudapp.azure.com

python3 manage.py runserver 0.0.0.0:8000
python3 ~/MacMailing/app/manage.py runserver 0.0.0.0:8000
```




crontab -e
@reboot nohup python3 ~/projets/MacMailing/app/manage.py runserver 0.0.0.0:8000>app.log & 