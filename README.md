# Azure AI with Python

Access Microsoft Azure AI and its cognitive services using Python, and Flask.

## Virtual Environment (optional)

We activate the virtual environment.

On Linux:
```
# sudo apt-get install -y python3-pip python3-venv # Libraries needed
python3 -m venv my_venv # Do this to invoke the module and create our environment called 'my_venv'
source ./my_venv/bin/activate
```
On Windows:
```
python -m venv my_venv # Do this to invoke the module and create our environment called 'my_venv'
.\.my_venv\Scripts\activate
```

## Libraries

This project is using:
```
pip install flask python-dotenv requests pytest
```

Alternatively, we can automate this process by adding the list of modules to a <b>requirements.txt</b>. To create one with the current modules installed in our environment:
```
pip freeze >> requirements.txt
```

Create this file for later use in our Dockerfile. It should look something like this:
```
flask
python-dotenv
requests
pytest

```

To install them:
```
pip install -r requirements.txt
```

# Using Dockerfile

Build the Docker image:
```
docker build -t my-python-app .
```
Run the image:
```
docker run -p 5000:5000 my-python-app
```

## Azure Portal

This application uses a valid subscription to Azure Portal with Translator and other services. To be able to use your own endpoint, the information must be stored in a <b>.env</b> file:
```
touch .env
```
Save your key-values like this:
```
KEY=your_key
ENDPOINT=your_endpoint
LOCATION=your_location
```

## Web Server

Set the environment variables:
```
# Windows
set FLASK_ENV=development
```
```
# Linux/macOS
export FLASK_ENV=development
```


Run <b>app.py</b>:
```
py app.py
```
or:
```
flask run
```

This should run the web application on localhost (port 5000):
</br>
<a target="_blank" href="http://127.0.0.1:5000/">http://127.0.0.1:5000/</a>


# Resources

## Python (Spanish)

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
