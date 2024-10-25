# syntax=docker/dockerfile:1

# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /ai-python-app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Expose the port the app runs on:
# 5000 for the Flask app (default)
# 443 for the HTTPS
# 80 for the HTTP
EXPOSE 80

# Define the command to run the application
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0:80"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]