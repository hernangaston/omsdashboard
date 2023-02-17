# LEVANTAR EL PROYECTO

1-instalar python version 3.7
    (use esa porque es la que pide AWS pensando que algun dia se puede usar)
    pueden usar pipenv para generar un entorno virtual


2-instalar pipenv


    -LINUX
      -$ sudo pip install pipenv
      
      
    -WINDOWS
        pip install pipenv


3-crear el entorno virtual con la version especifica de python
    pipenv
    
    

    pipenv --python 3.7
    
    
        o
        
        
    python3 -m pipenv --python 3.7



4-activar el entorno pipenv shell



5-instalar los paquetes
$ pipenv install -r requirements.txt



6-desplegar el servidor local
    dentro de la carpeta donde donde esta el archivo manage.py correr lo siguiente:
### python manage.py runserver
