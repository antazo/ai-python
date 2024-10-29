# syntax=docker/dockerfile:1

# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /ai-python-app

# Copy the requirements file into the container
COPY requirements.txt .

# Ensure that our container doesn't go to sleep
#CMD tail -f /dev/null

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Expose the port the app runs on:
EXPOSE 80
EXPOSE 443
EXPOSE 5000

# Define the command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]