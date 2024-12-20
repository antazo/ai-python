# AI with Python (Azure AI)

Harness AI advanced capabilities in a Pythonic way.  The DotNet version of this repository is [here](https://github.com/antazo/ai-dotnet).

A valid subscription is needed for your own endpoints. The project uses virtual environments, continuous integration pipelines, and containerization as optional. This repository is automatically deployed to container registries (Docker Hub and ACR) through GitHub Actions workflows.

Cognitive services used (so far):

* Neural Machine Translation (NMT): Translator.
* Convolutional Neural Networks (CNN): Computer Vision, Face.

Technologies used: Python, Flask, Pytest, unittest, Selenium, Swagger, GSAP, Docker, Minikube.

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
* [Resources](#resources)
  * [Azure](#azure)
  * [Azure AI](#azure-ai)

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

### Libraries

This project is using:

```bash
pip install flask flask-swagger-ui python-dotenv requests azure-mgmt-compute
```

[!Web testing]
Selenium is not included in the workflow, run it manually.

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

This application uses a valid subscription to Azure AI Services and Cognitive APIs to be able to use Language, Vision (Computer Vision, Custom Vision, Face), Decision, Speech, Metrics Advisor, and Document Intelligence.

Create a single resource for all of them, your Keys and Endpoints information must be stored in a **.env** file.

Note that the Translator service uses its own endpoint. Save your key-values like this:

```plaintext
LOCATION=
AI_SERVICES_KEY=
AI_SERVICES_ENDPOINT=
TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com/
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

<http://127.0.0.1/>

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

This repository integrates ACR in the GitHub Actions workflow. All the following steps are already automated in the **ci-acr.yml** file:

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
az container create \
    --resource-group [AZURE_RESOURCE_GROUP] \
    --name ai-python-app \
    --image aipython.azurecr.io/ai-python-app:v1 \
    --cpu 1 \
    --memory 1 \
    --registry-login-server aipython.azurecr.io \
    --registry-username aipython \
    --registry-password [ACR_PASSWORD] \
    --ip-address Public \
    --dns-name-label aidemo \
    --ports 80
```

Try it:

<http://aidemo.northeurope.azurecontainer.io/>

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
* AZURE_CREDENTIALS: Azure service principal credentials in JSON format (**acr-credentials.json**).

## Resources

### Azure

[Getting started with Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-get-started)\
[Create an Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)\
[Create a single database - Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal)\
[Use the Azure portal to create a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/quick-create-portal)\
[Create a Windows virtual machine in the Azure portal](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-portal)\
[Host a web application with Azure App Service](https://learn.microsoft.com/en-us/training/modules/host-a-web-app-with-azure-app-service/)\
[Deploy and run a containerized web app with Azure App Service](https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/)\
[Create a container image for deployment to Azure Container Instances](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-tutorial-prepare-app)\
[Deploy a container instance in Azure using the Azure portal](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-quickstart-portal)

### Azure AI

[Azure Portal](https://portal.azure.com?azure-portal=true)\
[Azure AI Studio](https://ai.azure.com/)\
[Vision Studio](https://portal.vision.cognitive.azure.com?azure-portal=true)\
[Language Studio](https://language.cognitive.azure.com)\
[Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)\
[Sample documents](https://aka.ms/mslearn-receipt)\
[OneDrive](https://onedrive.live.com)

#### Labs

[Lab Environment Setup](https://microsoftlearning.github.io/AI-102-AIEngineer/Instructions/00-setup.html)\
[Azure AI Vision documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)\
[Create computer vision solutions with Azure AI Vision](https://learn.microsoft.com/en-us/training/paths/create-computer-vision-solutions-azure-ai/)\
[Create Translator service](https://learn.microsoft.com/en-us/training/modules/python-flask-build-ai-web-app/5-exercise-create-translator-service)\
[Lab files for Azure AI Vision modules](https://github.com/MicrosoftLearning/mslearn-ai-vision)\
[Lab 01 - Machine Learning: Explore Automated Machine Learning in Azure Machine Learning](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Labs/01-machine-learning.html)\
[Lab 02 - Content Safety: Explore Azure AI Services](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Labs/02-content-safety.html)\
[Lab 11 - Explore an Azure AI Search index (UI)](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Labs/11-ai-search.html)\
[Lab 12 - Explore Microsoft Copilot in Microsoft Edge](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Labs/12-generative-ai.html)\
[Explore the components and tools of the Azure AI Studio](https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/01-Explore-ai-studio.html)\
[Explore space with Python and Visual Studio Code; inspired by Netflix's Over the Moon](https://learn.microsoft.com/en-us/training/paths/explore-space-using-python/)
