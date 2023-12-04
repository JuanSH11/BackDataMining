# Proyecto de grado GITSIGHT PRO

## Autores
Alejandro Ahogado Prieto (a.ahogado@uniandes.edu.co)
Juan Sebastián Hoyos Muñoz (js.hoyosm@uniandes.edu.co)

## Descripción

Este repositorio contiene el código desarrollado como parte de la tesis GITSIGHT PRO. El objetivo de este proyecto es proveer las herramientas necesarias para la creación de un análisis de repositorios públicos de GitHub, de forma que se puedan encontrar ciertas tendencias en la efectividad y eficiencia de los desarrolladores, tras haber recolectado, transformado y presentado la información.

## Requisitos 

Asegurate de tener instalado python 3.9 (este se testeó específicamente con Python 3.9.2rc1) ya que algunas de las librerías utilizadas pueden presentar incompatibilidades con otras versiones. De igual manera, es necesario tener instalado y configurado postgreSQL 16.

Es necesario que se cree manualmente la base de datos llamada datamining_db, asignada al usuario postgres. Solo es necesario que esté creada, los esquemas y modelos se cargarán automáticamente al iniciar la aplicación.

Una vez realizado lo anterior, ejecuta el archivo "requirements.txt" encontrado en la raíz del proyecto.

Finalmente, ejecuta el archivo "start_server.sh" encontrado en la raiz del proyecto. (En bash ejecuta ./start_server.sh)*
- Si quieres finalizar el proceso en git bash usa ctrl+c

*Es importante tener en cuenta que siempre que se inicie la aplicación desde cero al ejecutar este archivo, se limpiará la base de datos, por lo que en la consola te pedirá indicar la clave asignada a la base de datos. Cuando no se detiene por completo la aplicación y se realizan nuevos análisis, este procedimiento se realiza automáticamente.

Dependiendo tu sistema operativo y configuración es posible que debas brindar ciertos permisos para poder ejecutar la aplicación.

## Usuario administrador
En caso de que seas el nuevo administrador de la aplicación, en esta se implementó la autenticación con GitHub, por lo que esta debe estar registrada en OAuth Apps para poder usarla. 

Si quieres registrarla desde cero, dirigete a tu cuenta de GitHub, en la sección de settings, developer settings, encontrarás OAuth Apps. En este caso se configuró con la siguiente información:
- Name: DataMining
- Homepage URL: http://localhost:8000
- Authorization callback URL: http://localhost:8000/callback

Una vez realices el procedimiento anterior, se te generará un Client ID y Client Secret el cuál deberas reemplazar en el archivo views.py (GITHUB_CLIENT_ID y GITHUB_CLIENT_SECRET). Esta configuración se maneja de esta manera ya que actualmente el proyecto es privado, sin embargo, si deseas aumentar la seguridad puedes manejar los secretos en tu ambiente y realizar la respectiva configuración o hacer uso de AWS secrets o algo por el estilo.