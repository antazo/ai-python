# ai-python

Access Microsoft Azure AI and its cognitive services using Python.

## Virtual Environment (optional)

We activate the virtual environment. On Linux:
```
# sudo apt-get install -y python3-pip python3-venv # Libraries needed
# python3 -m venv my_venv # Do this to invoke the module and create our environment called 'my_venv'
source ./my_venv/bin/activate
```
On Windows:
```
# python -m venv my_venv # Do this to invoke the module and create our environment called 'my_venv'
.\.my_venv\Scripts\activate
```

## Libraries

This project is using:
```
pip install Flask
pip3 install -U selenium
pip install webdriver-manager
pip install pillow # We need PIL to open the screenshots created by selenium
```

Alternatively, we can automate this process by adding the list of modules to a <b>requirements.txt</b>. To create one with the current modules installed in our environment:
```
pip freeze >> requirements.txt
```

Create this file for later use in our Dockerfile. It should look like this:
```
flask
python-dotenv
requests
```

To install them:
```
pip install -r requirements.txt
```

# Resources

## Python

1. Python para principiantes
* https://learn.microsoft.com/es-es/training/paths/beginner-python/

2. Compilación de aplicaciones reales con Python
* https://learn.microsoft.com/es-es/training/paths/python-language/

3. Uso de conceptos básicos de Python para resolver misterios y buscar respuestas
* https://learn.microsoft.com/es-es/training/paths/python-partnership/

4. Rol de Python en la exploración espacial
* https://learn.microsoft.com/es-es/training/paths/introduction-python-space-exploration-nasa/

5. Explore el espacio con Python y Visual Studio Code (inspirado la película de Netflix Más allá de la luna)
* https://learn.microsoft.com/es-es/training/paths/explore-space-using-python/
