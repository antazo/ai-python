# Azure AI with Python

Access Microsoft Azure AI and its cognitive services using Python, and Flask. A valid subscription to Azure is needed for your endpoints.

This repository uses virtual environments, CI pipelines (GitHub Actions), Docker, and Kubernetes as optional.

## Installation

Clone (or fork) this git repository:

```bash
git clone https://github.com/antazo/ai-python.git
cd ai-python
```

### Virtual Environment

If we want to use a virtual environment, we need to invoke the **venv** module, and activate it. In my case, I'm calling it **my_env**:

On Linux/macOS:

```bash
# sudo apt-get install -y python3-pip python3-venv # Libraries needed
python3 -m venv my_venv
source ./my_venv/bin/activate
```

On Windows:

```powershell
py -3 -m venv my_venv
.\.my_venv\Scripts\activate
```

## Libraries

This project is using:

```bash
pip install flask flask-swagger-ui python-dotenv requests pytest
```

Optionally, we can automate this process by adding the list of modules to **requirements.txt**. To create one with the current modules installed in our environment:

```bash
pip freeze >> requirements.txt
```

Create this file for later use in our Dockerfile or CI pipeline. It should look something like this:

```plaintext
flask
flask-swagger-ui
python-dotenv
requests
pytest

```

To install them:

```bash
pip install -r requirements.txt
```

## Azure Portal

This application uses a valid subscription to Azure Portal with Translator and other services. To be able to use your own endpoint, the information must be stored in a **.env** file:

```bash
touch .env
```

Save your key-values like this:

```plaintext
KEY=your_key
ENDPOINT=your_endpoint
LOCATION=your_location
```

## Using local Web Server

Set the environment variables.

On Linux/macOS:

```bash
export FLASK_ENV=development
```

On Windows:

```powershell
set FLASK_ENV=development
```

Run **app.py**:

```bash
py app.py
```

or:

```bash
flask run
```

This should run the web application on localhost (port 5000):  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Using Dockerfile

Build the Docker image:

```bash
docker build -t ai-python-app .
```

Run the image:

```bash
docker run -p 5000:5000 ai-python-app
```

## Using Kubernetes (Minikube)

Start K8s:

```bash
minikube start --driver=docker
```

Build the Docker image inside Minikube:

```bash
eval $(minikube -p minikube docker-env)
# if "eval" isn't working, you must be using CMD on Windows. In that case, do it manually, copy&paste.
# You need to point the shell to minikube's docker-daemon before building the Docker image.
docker build -t ai-python-app .
```

Apply the Deployment and Service YAML files:

```bash
kubectl apply -f static/deployment.yaml
kubectl apply -f static/service.yaml
kubectl apply -f static/pod.yaml
```

Access the Flask application:

```bash
minikube service ai-flask-app-service
```

Troubleshoot:

```bash
kubectl get pods
kubectl describe pod ai-flask-app
kubectl get services
kubectl describe service ai-flask-app-service
```

## Resources

## Python (Spanish)

1. Python para principiantes

    * <https://learn.microsoft.com/es-es/training/paths/beginner-python/>

2. Compilación de aplicaciones reales con Python

    * <https://learn.microsoft.com/es-es/training/paths/python-language/>

3. Uso de conceptos básicos de Python para resolver misterios y buscar respuestas

    * <https://learn.microsoft.com/es-es/training/paths/python-partnership/>

4. Rol de Python en la exploración espacial

    * <https://learn.microsoft.com/es-es/training/paths/introduction-python-space-exploration-nasa/>

5. Explore el espacio con Python y Visual Studio Code (inspirado la película de Netflix Más allá de la luna)

    * <https://learn.microsoft.com/es-es/training/paths/explore-space-using-python/>
