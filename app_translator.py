#!/usr/bin/env python3
# app_translator.py

import os, requests, uuid
from flask import Blueprint, render_template, request

app_translator_bp = Blueprint('translator', __name__)

@app_translator_bp.route('/translator', methods=['GET'])
def translator():
    return render_template('translator.html')

@app_translator_bp.route('/translator', methods=['POST'])
def translator_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['AI_SERVICES_KEY']
    endpoint = os.environ['TRANSLATOR_ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    try:
        translated_text = translator_response[0]['translations'][0]['text']
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        translated_text = f"An error occurred, check your Keys and Endpoints: {e}"
    except (KeyError, IndexError) as e:
        # Handle any errors in parsing the JSON response
        translated_text = f"An error occurred while parsing the response, check your Keys and Endpoints: {e}"
    except Exception as e:
        # Handle any other exceptions
        translated_text = f"An unexpected error occurred: {e}"

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'translator_results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )