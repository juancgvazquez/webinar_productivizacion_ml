Este repositorio se utilizó para un webinar y clase de puesta en productivo de modelos de data science. En ese sentido, consta, básicamente, de 5 alternativas.

1. Productivización mediante Notebooks (carpeta notes-pipelines/notebooks)
    
        En este caso, se utilizan los notebooks como herramienta de productivización y se trabaja primero sobre uno que se llama Data Analysis. Luego el código se limpia en tres procesos, que se llaman en forma de pipelines a partir de la librería papermill. Para ejecutar el primero, desde la línea de comando, se debe utilizar el comando:
                papermill 1-preprocess.ipynb 1-preprocess-run.ipynb
            
            y se le pueden pasar parámetros vía el argumento 
            
            -p nombredeparametro valordeparametro

2. Productivización mediante código para automatizar (carpeta automatización)

        Aquí ya se armaron funciones para cada uno de los procesos (preprocess, train, predict) y se utilizan como módulo, llamandolos desde una función main. Para correrlo, se ejecuta el comando:

            python main.py

3. Productivización mediante código para automatizar + cli (carpeta automatización + cli)

        Igual al anterior sólo que aquí se realiza un interprete de línea de comando. Para ejecutarlo se utilizar:

            python main.py comando
        
        Para más información ver el help del comando

4. Productivización vía API (carpeta fastapi_skeleton)

        El primer método máduro. Se construye una API con distintos métodos y endpoints para acceder. En este caso, para ejecutarlo, debido a que se construyo con FASTAPI, se debe utilizar el comando:

            uvicorn fastapi_skeleton.main:app
        
        Y luego entrar desde un navegador a http://localhost:8000/docs para acceder a la documentación.

5. Productivización vía API + Interfaz de Usuario (carpeta api-dash)

        Es el mismo método que el anterior, sólo que se le agrega un tablero de interfaz de usuario. Para utilizarlo se debe lanzar la API anterior, y en otra terminal, lanzar la interfaz con el comando:
            python api-dash.py
        
        Luego acceder a http://localhost:8050 y podremos ver la interfaz desarrollada en dash. En la carpeta se encuentra dos archivos csvs que permiten realizar una predicción, uno con un sólo dato y otro con múltiples datos.

Ademas hay un notebook llamado notebookdewebinar que permite ver cómo se contactaría con la API (método 4), una vez funcionando, desde python.

Finalmente agregamos una aplicación muy sencilla de tareas para que se entienda mejor el concepto de APIs, en al archivo simpletaskapi.py. Se lanza ejecutando python simpletaskapi.py.