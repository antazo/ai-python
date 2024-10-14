#!/usr/bin/env python3
import json
from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

@app.route('/')
def start():
    name = request.args.get('name', 'visitor')
    body = f"<h1>Hello {name}!</h1>"
    body += f"<p>This is created with Flask. These are the endpoints with examples:</p>"
    body += f"<p><a href=\"translator\">/translator</a></p>"
    body += f"<p><a href=\"hello?name=Alex\">/hello?name=Alex</a></p>"
    body += f"<p><a href=\"bye?name=Alex\">/bye?name=Alex</a></p>"
    body += f"<p><a href=\"planet_distances\">/planet_distances</a></p>"
    body += f"<p><a href=\"generate_report?main_tank=80&external_tank=80&hydrogen_tank=75\">/generate_report?main_tank=80&external_tank=80&hydrogen_tank=75</a></p>"
    return body

@app.route('/translator', methods=['GET'])
def translator():
    return render_template('translator.html')

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

@app.route('/foobar')
def foobar():
    body = f"<h1>Hello!</h1>"

    return body

if __name__ == '__main__':
    app.run(debug=True, port=5000)