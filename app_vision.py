#!/usr/bin/env python3
# app_vision.py

import os, requests
from flask import Blueprint, render_template, request

app_vision_bp = Blueprint('vision', __name__)

@app_vision_bp.route('/vision', methods=['GET'])
def vision():
    return render_template('vision.html')

@app_vision_bp.route('/vision', methods=['POST'])
def vision_post():
    # Read the image from the form
    image = request.files['image']

    # Save the uploaded image to a directory
    image_filename = image.filename
    image_path = os.path.join('uploads', image_filename)
    image.save(image_path)

    # Load the values from environment variables
    key = os.environ.get('AI_SERVICES_KEY')
    endpoint = os.environ.get('AI_SERVICES_ENDPOINT')

    # Indicate that we want to analyze the image and the API version (3.2)
    path = '/vision/v3.2/analyze'
    # Add the visual features parameter
    visual_features = 'Categories,Description,Color'
    # Create the full URL
    constructed_url = f"{endpoint}{path}?visualFeatures={visual_features}"

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/octet-stream'
    }

    try:
        # Make the request
        with open(image_path, 'rb') as image_data:
            response = requests.post(constructed_url, headers=headers, data=image_data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        vision_response = response.json()
        description = vision_response['description']['captions'][0]['text']
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        description = f"An error occurred, check your Keys and Endpoints: {e}"
    except (KeyError, IndexError) as e:
        # Handle any errors in parsing the JSON response
        description = f"An error occurred while parsing the response, check your Keys and Endpoints: {e}"
    except Exception as e:
        # Handle any other exceptions
        description = f"An unexpected error occurred: {e}"

    return render_template('vision.html', description=description, image_path=image_path)
