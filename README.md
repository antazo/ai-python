# Azure AI with Python

Access Microsoft Azure AI advanced capabilities (cognitive services) using Python. A valid subscription to Azure is needed for your own endpoints.

The project uses virtual environments, CI pipelines, and containerization as optional.

This repository is automatically deployed to container registries (Docker Hub and ACR) through GitHub Actions workflows.

## Overview

* [Installation](#installation)
  * [Virtual Environment (optional)](#virtual-environment-optional)
* [Libraries](#libraries)
* [Azure Portal](#azure-portal)
* [Deployment](#deployment)
  * [Using local Web Server](#using-local-web-server)
  * [Using Dockerfile](#using-dockerfile)
  * [Using Kubernetes (Minikube)](#using-kubernetes-minikube)
* [Pushing the images to container registries](#pushing-the-images-to-container-registries)
  * [Docker Hub](#docker-hub)
  * [Azure Container Registry (ACR)](#azure-container-registry-acr)
* [Container registries and GitHub Actions workflow](#container-registries-and-github-actions-workflow)
  * [CI Docker Hub](#ci-docker-hub)
  * [CI Azure Container Registry (ACR)](#ci-azure-container-registry-acr)

## Installation

Clone (or fork) this git repository:

```bash
git clone https://github.com/antazo/ai-python.git
cd ai-python
```

### Virtual Environment (optional)

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
pip install flask flask-swagger-ui python-dotenv requests azure-mgmt-compute
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
azure-mgmt-compute

```

To install them:

```bash
pip install -r requirements.txt
```

## Azure Portal

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

## Deployment

### Using local Web Server

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

### Using Dockerfile

To containerize this application, build the Docker image by using the Dockerfile included:

```bash
docker build -t ai-python-app .
```

Run the image:

```bash
docker run -it -p 80:80 ai-python-app
# -it lets you stop it with Ctrl+C
```

Try it:  
[http://127.0.0.1/](http://127.0.0.1/)

### Using Kubernetes (Minikube)

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

Apply the Deployment and Service YAML files. Inside **deployment.yaml** you should point to your Docker image ("image: [DOCKER_USERNAME]/ai-python-app:latest"):

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

## Pushing the images to container registries

### Docker Hub

Tag the Docker image (don't forget to replace [DOCKER_USERNAME]!):

```bash
docker tag ai-python-app:latest [DOCKER_USERNAME]/ai-python-app:latest
```

Log in to your Docker Hub:

```bash
docker login
```

Push the Docker image:

```bash
docker push [DOCKER_USERNAME]/ai-python-app:latest
```

You can use the image from my Docker Hub for integration tests (the keys are not valid for E2E tests):
[https://hub.docker.com/repository/docker/antazo/ai-python-app/general](https://hub.docker.com/repository/docker/antazo/ai-python-app/general)

### Azure Container Registry (ACR)

This repository integrates ACR in the GitHub Actions workflow. All the following steps are already automated in the **python-app.yml** file:

Log in to your Azure CLI:

```powershell
az login
```

Create your ACR in your own resource group (replace [AZURE_RESOURCE_GROUP]). My registry will be called **aipython**:

```powershell
az acr create --resource-group [AZURE_RESOURCE_GROUP] --name aipython --sku Basic
```

Login to the ACR we just created:

```powershell
az acr login --name aipython
```

Show the ACR login server, and then use it to create a tag:

```powershell
az acr show --name aipython --query loginServer --output table
```

In my case, it's **aipython.azurecr.io**:

```powershell
docker tag ai-python-app aipython.azurecr.io/ai-python-app:v1
```

Push the image to the ACR (this step is not needed in the YAML file):

```powershell
docker push aipython.azurecr.io/ai-python-app:v1
```

List the repository, and the tags:

```powershell
az acr repository list --name aipython --output table
# is it "ai-python-app"?
az acr repository show-tags --name aipython --repository ai-python-app --output table
# is it "v1"?
```

Create the container. You will also need to check your Access Keys and privileges to be able to replace [ACR_PASSWORD]. The DNS label will be **aidemo**:

```powershell
az container create --resource-group [AZURE_RESOURCE_GROUP] --name ai-python-app --image aipython.azurecr.io/ai-python-app:v1 --cpu 1 --memory 1 --registry-login-server aipython.azurecr.io --registry-username aipython --registry-password [ACR_PASSWORD] --ip-address Public --dns-name-label aidemo --ports 80
```

Try it:
[http://aidemo.northeurope.azurecontainer.io/](http://aidemo.northeurope.azurecontainer.io/)

## Container registries and GitHub Actions workflow

### CI Docker Hub

All you need to do is add your Docker credentials to secrets:

* DOCKER_USERNAME
* DOCKER_PASSWORD

Now, enable the workflow.

### CI Azure Container Registry (ACR)

First, add these information to your secrets:

* AZURE_RESOURCE_GROUP: Name of your Azure resource group.
* ACR_USERNAME: The registry admin username.
* ACR_PASSWORD: The registry password.

Create a role assignment (RBAC) to be able to pull and push as a **Contributor** (in other cases we would use **acrpull** or  **acrpush** for least privileges):

```powershell
az ad sp create-for-rbac \
    --name "http://ai-python-sp" \
    --role Contributor \
    --scopes /subscriptions/[AZURE_SUBSCRIPTION_ID]/resourceGroups/[AZURE_RESOURCE_GROUP]/providers/Microsoft.ContainerRegistry/registries/aipython \
    --sdk-auth > acr-credentials.json
```

This will output a JSON to the file **acr-credentials.json** with the rest of information needed for your secrets. Add them to make the workflow work:

* AZURE_CLIENT_ID: The client ID of your Azure service principal.
* AZURE_CLIENT_SECRET: The client secret of your Azure service principal.
* AZURE_SUBSCRIPTION_ID: The subscription ID of your Azure service.
* ~~AZURE_TENANT_ID: The tenant ID of your Azure subscription.~~
* AZURE_CREDENTIALS: Azure service principal credentials in JSON format (**acr-credentials.json**).

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
