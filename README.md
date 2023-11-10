Lemo Miniblog 2 en Flask
======================
Un miniblog/clon de twitter realizado con Flask y SQLAlchemy, que cuenta con una implementación de una API para consultar información sobre los usuarios, posteos, comentarios y categorías.

## Tecnologías usadas
 - Flask
 - SQLAlchemy
 - Bootstrap
 - Python
 - Docker
 - HTML

## Capturas

<img src="https://i.ibb.co/wsFttrx/miniblog-muro.png" alt="miniblog-muro" border="0">

----

<img src="https://i.ibb.co/B4cSyH9/miniblog-filter1.png" alt="miniblog-filter1" border="0">

----

<img src="https://i.ibb.co/Tq9jw6H/miniblog-user.png" alt="miniblog-user" border="0">

----

<img src="https://i.ibb.co/DWbc0b1/miniblog-edit.png" alt="miniblog-edit" border="0">

## Set-Up

Para correr este projecto, lo podemos hacer de manera local o virtualizando la aplicación con Docker. 

## Corriendo el programa con Docker:
Para virtualizarlo y correrlo con Docker, es necesario tener los servicios de [Docker](https://www.docker.com/) instalados. Usaremos comandos de docker y docker-compose.

Primero clonamos el repositorio de manera local. Luego, en la carpeta clonada deberemos crear un archivo ".env" donde necesitamos almacenar nuestras credenciales de acceso. Para saber como completar este archivo, necesitarás guiarte de ".env.example", donde habrá un modelo con los nombres de variables que usa el programa.
Una vez realizado el '.env', abriremos la terminal y escribiremos:
```bash
  sudo docker-compose build
```
y, cuando termine de construirse la imagen de docker que contiene nuestra aplicación, haremos el siguiente comando para correr el contenedor:
```bash
  sudo docker-compose up
```
De estar bien puestas las credenciales, en la terminal debería indicar que el contenedor está andando y siendo accesible desde [localhost:5040](http://localhost:5040/).

Si estuviesemos en Windows, el proceso sería igual, sólo que en la terminal no tendríamos que hacer uso de "sudo", es decir, escribir directamente "docker-compose build" y "docker-compose up".

## Corriendo el programa de manera local con Xampp:
Para correrlo local se necesita una versión actualizada de python y [Xampp](https://www.apachefriends.org/es/index.html) para simular la base de datos de manera local. Se deben seguir los siguientes pasos:

Primero debemos clonar el repositorio de manera local.
Una vez lo tenemos, debemos crearle un entorno virtual con python e instalarle los requerimientos provistos, que incluyen Flask y SQLAlchemy, entre otros.
Creamos el entorno virtual con el siguiente comando:
```bash
  python3 -m venv venv
```
Ahora debemos ingresar dentro del entorno para instalarle los requerimientos. 
Si estamos en LINUX, lo hacemos con el siguiente comando:
```bash
  source venv/bin/activate
```
En cambio, en WINDOWS es de la siguiente manera:
```bash
   venv/Scripts/activate
```
Una vez activado el entorno virtual, le vamos a instalar los requerimientos con el siguiente comando:
```bash
  pip install -r requirements.txt
```
---
Ahora, sin cerrar la terminal, abriremos [Xampp](https://www.apachefriends.org/es/index.html) e iniciaremos sus servicios.
En windows puede ser abierto su acceso directo, pero en linux debemos ingresar el siguiente comando:
```bash
  sudo /opt/lampp/manager-linux-x64.run
```
Una vez abierto, y con sus servicios inicializados, queda crear e iniciar la base de datos.
Ingresaremos al módulo de [base de datos de Xampp](http://localhost/phpmyadmin/index.php?route=/server/databases) y la creamos con el siguiente nombre:
```bash
  lemo_miniblog
```
de tener otro nombre la aplicación NO FUNCIONARÁ.
Para iniciarla, volveremos a la terminal donde tenemos activado el entorno virtual e ingresaremos los siguientes comandos:
```bash
  flask db init
  flask db migrate -m "creacion de tablas"
  flask db upgrade
```
---

y finalmente, corremos el proyecto con un:
```bash
  flask run
```
y accedemos a [localhost:5000](http://localhost:5000/). Con eso, estás listo para disfrutar el miniblog!


## Autor
Hecho con mucho cariño por [@Facundo Lemo](https://github.com/FacundoEsteban-Lemo).

