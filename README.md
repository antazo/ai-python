# Azure AI with Python

Access Microsoft Azure AI and its cognitive services using Python, and Flask.

## Virtual Environment

If we want to use a virtual environment, we need to invoke the <b>venv</b> module, and activate it. In my case, I'm calling it <b>my_env</b>:

On Linux:
```
# sudo apt-get install -y python3-pip python3-venv # Libraries needed
python3 -m venv my_venv
source ./my_venv/bin/activate
```
On Windows:
```
python -m venv my_venv
.\.my_venv\Scripts\activate
```

## Libraries

This project is using:
```
pip install flask flask-swagger-ui python-dotenv requests pytest
```

Optionally, we can automate this process by adding the list of modules to <b>requirements.txt</b>. To create one with the current modules installed in our environment:
```
pip freeze >> requirements.txt
```

Create this file for later use in our Dockerfile or CI pipeline. It should look something like this:
```
flask
flask-swagger-ui
python-dotenv
requests
pytest

```

To install them:
```
pip install -r requirements.txt
```


# Azure Portal

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

# Using local Web Server

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


# Using Dockerfile

Build the Docker image:
```
docker build -t ai-python-app .
```
Run the image:
```
docker run -p 5000:5000 ai-python-app
```

# Using Kubernetes (Minikube)

Start K8s:
```
minikube start --driver=docker
```

Build the Docker image inside Minikube:
```
eval $(minikube -p minikube docker-env)
# if "eval" isn't working, you must be using CMD on Windows. In that case, do it manually, copy&paste
docker build -t ai-python-app .
```

Apply the Deployment and Service YAML files:
```
kubectl apply -f static/deployment.yaml
kubectl apply -f static/service.yaml
```

Access the Flask application:
```
minikube service flask-app-service
```

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
