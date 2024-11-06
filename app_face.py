#!/usr/bin/env python3
# app_face.py

import os, requests
from flask import Blueprint, render_template, request

app_face_bp = Blueprint('face', __name__)

@app_face_bp.route('/face', methods=['GET'])
def face():
    return render_template('face.html')

@app_face_bp.route('/face', methods=['POST'])
def face_post():
    # Read the image from the form
    image = request.files['image']

    # Load the values from environment variables
    key = os.environ.get('AI_SERVICES_KEY')
    endpoint = os.environ.get('AI_SERVICES_ENDPOINT')

    # Indicate that we want to analyze the image and the API version (v1.0)
    path = '/face/v1.0/detect'
    # Add the parameters for face detection
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion'
    }
    # Create the full URL
    constructed_url = endpoint + path

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/octet-stream'
    }

    try:
        # Make the request
        response = requests.post(constructed_url, headers=headers, params=params, data=image.read())
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        face_response = response.json()
        if face_response:
            description = f"Detected {len(face_response)} face(s)."
            for face in face_response:
                attributes = face['faceAttributes']
                description += f"\n- Age: {attributes['age']}, Gender: {attributes['gender']}, Smile: {attributes['smile']}, Emotion: {attributes['emotion']}"
        else:
            description = "No faces detected."
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        description = f"An error occurred, check your Keys and Endpoints. The resource you are trying to call has limited access, or must be approved to use that capability: {e}"
    except (KeyError, IndexError) as e:
        # Handle any errors in parsing the JSON response
        description = f"An error occurred while parsing the response, check your Keys and Endpoints. The resource you are trying to call has limited access, or must be approved to use that capability: {e}"
    except Exception as e:
        # Handle any other exceptions
        description = f"An unexpected error occurred: {e}"

    return render_template('face.html', description=description)
