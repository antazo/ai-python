#!/usr/bin/env python3
# app.py

import os, json
from flask import Flask, redirect, url_for, request, render_template, render_template_string
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

# Import bluprints from the app_*.py files
from app_translator import app_translator_bp
from app_vision import app_vision_bp
from app_face import app_face_bp
from app_game import app_game_bp

load_dotenv()

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    name = request.args.get('name', 'visitor')
    return render_template(
        'home.html',
        name=name
    )

# Register the blueprints
app.register_blueprint(app_translator_bp)
app.register_blueprint(app_vision_bp)
app.register_blueprint(app_face_bp)
app.register_blueprint(app_game_bp)

@app.route('/planet_distances')
def planet_distances():
    distances = {
        "Mercury": 91.7,
        "Venus": 41.4,
        "Earth": 0.0,
        "Mars": 78.3,
        "Jupiter": 628.7,
        "Saturn": 1277.4,
        "Uranus": 2721.8,
        "Neptune": 4351.4
    }

    # Convert dictionary to JSON string
    json_data = json.dumps(distances)
    return json_data

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)