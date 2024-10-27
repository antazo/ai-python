#!/usr/bin/env python3
import json
import random
from flask import Flask, redirect, url_for, request, render_template, render_template_string, session
import requests, os, uuid
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

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

@app.route('/translator', methods=['GET'])
def translator():
    return render_template('translator.html')

@app.route('/translator', methods=['POST'])
def translator_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
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
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

@app.route('/computer_vision', methods=['GET'])
def computer_vision():
    return render_template('computer_vision.html')

@app.route('/computer_vision', methods=['POST'])
def computer_vision_post():
    # Handle the POST request for computer vision
    image = request.files['image']
    # Process the image using a computer vision library or API
    result = "Processed Image Result"  # Example result
    return render_template('computer_vision.html', result=result)

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Alex')
    return f"Hello {name}!"

@app.route('/bye')
def bye():
    name = request.args.get('name', 'Alex')
    return f"Goodbye {name}!"

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

@app.route('/generate_report')
def generate_report():
    main_tank = request.args.get('main_tank', '80')
    external_tank = request.args.get('external_tank', '70')
    hydrogen_tank = request.args.get('hydrogen_tank', '75')
    output = f"""Fuel Report:
    Main tank: {main_tank}
    External tank: {external_tank}
    Hydrogen tank: {hydrogen_tank} 
    """
    return output

@app.route('/game')
def game():
    class GameRockPaperScissors:
        def __init__(self):
            self.player = None
            self.enemy = None
            self.switcher = {
                "rock": 0,
                "paper": 1,
                "scissors": 2,
                "lizard": 3,
                "spock": 4
            }
            self.rules = [
                [0, -1, 1, 1, -1],
                [1, 0, -1, -1, 1],
                [-1, 1, 0, 1, -1],
                [-1, 1, -1, 0, 1],
                [1, -1, 1, -1, 0]
            ]

        def toNumericalChoice(self, choice):
            return self.switcher[choice]

        def play(self):

            player_num = self.toNumericalChoice(self.player)
            enemy_num = self.toNumericalChoice(self.enemy)

            if self.rules[player_num][enemy_num] == 1:
                return "You win!"
            elif self.rules[player_num][enemy_num] == -1:
                return "You lose!"
            else:
                return "It's a tie!"

    game = GameRockPaperScissors()
    
    choices = list(game.switcher.keys())

    choicePlayer = request.args.get('choice').lower() if request.args.get('choice') in list(game.switcher.keys()) else None
    choiceEnemy = random.choice(list(game.switcher.keys()))
    
    result = None
    if choicePlayer:
        game.player = choicePlayer
        game.enemy = choiceEnemy
        result = game.play()
    return render_template(
        'rockpaperscissors.html',
        choices=choices,
        choicePlayer=choicePlayer,
        choiceEnemy=choiceEnemy,
        result=result
    )

@app.route('/foobar')
def foobar():

    class Foo:
        def __init__(self):
            self.a = 1
            self.b = 2

    class Bar:
        def __init__(self):
            self.c = 3
            self.d = 4

    foo = Foo()
    bar = Bar()

    html_content = f"<h1>/foobar</h1>"
    html_content += f"foo.a: {foo.a}<br>"
    html_content += f"bar.c: {bar.c}<br>"
    return html_content

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)