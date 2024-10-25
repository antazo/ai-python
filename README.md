# Azure AI with Python

Access Microsoft Azure AI advanced capabilities (Cognitive Services) using Python. A valid subscription to Azure is needed for your own endpoints:

* Translator
* Computer Vision (pending)

This repository uses virtual environments, CI pipelines (GitHub Actions), and containerization as optional.

## 1. Installation

Clone (or fork) this git repository:

```bash
git clone https://github.com/antazo/ai-python.git
cd ai-python
```

### 1.1 Virtual Environment (optional)

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

## 2. Libraries

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

## 3. Azure Portal

This application uses a valid subscription to Azure AI services to be able to use Translator, Vision and so on. Your endpoint information must be stored in a **.env** file:

```bash
nano .env
```

Save your key-values like this:

```plaintext
KEY=your_key
ENDPOINT=your_endpoint
LOCATION=your_location
```

## 4. Deployment

### 4.1 Using local Web Server

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
flask run -p 80
```

This should run the web application on localhost:  
[http://127.0.0.1/](http://127.0.0.1/)

### 4.2 Using Dockerfile

To containerize this application, build the Docker image by using the Dockerfile included:

```bash
docker build -t ai-python-app .
```

Run the image:

```bash
docker run -it -p 80:80 ai-python-app
# -it lets you stop it with Ctrl+C
```

### 4.3 Pushing the image to your own Docker Hub

Tag the Docker image (don't forget to replace [username]!):

```bash
docker tag ai-python-app:latest [username]/ai-python-app:latest
```

Log in to your Docker Hub:

```bash
docker login
```

Push the Docker image:

```bash
docker push [username]/ai-python-app:latest
```

You can use the image from my Docker Hub for integration tests (the keys are not valid for E2E tests):
[https://hub.docker.com/repository/docker/antazo/ai-python-app/general](https://hub.docker.com/repository/docker/antazo/ai-python-app/general)

### 4.4 Using Kubernetes (Minikube)

Start K8s and login your Docker:

```bash
minikube start --driver=docker
docker login
```

Point the shell to Minikube's docker-daemon before building the Docker image:

```bash
eval $(minikube -p minikube docker-env)
```

If "eval" isn't working, you must be using CMD on Windows. In that case, do it manually:.

```powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

Build the Docker image inside Minikube. Don't forget to login your Docker first:

```bash
docker build -t ai-python-app .
```

Apply the Deployment and Service YAML files. Inside **deployment.yaml** you should point to your Docker image ("image: [username]/ai-python-app:latest"):

```bash
kubectl apply -f static/deployment.yaml # Edit this file before applying!
kubectl apply -f static/service.yaml
```

Access the Flask application:

```bash
minikube service ai-flask-app-service
```

Troubleshoot:

```bash
kubectl get pods # Get the list of pods
kubectl describe pod ai-flask-app -n default 

kubectl get services # Get the list of services
kubectl describe service ai-flask-app-service
```

## Resources

### Python (Spanish)

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
