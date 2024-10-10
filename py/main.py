#!/usr/bin/env python3
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def start():
    name = request.args.get('name', 'visitor')
    body = f"<h1>Hello {name}!</h1>"
    body += f"<p>This is created with Flask. These are the endpoints with examples:</p>"
    body += f"<p><a href=\"hello?name=Alex\">hello?name=Alex</a></p>"
    body += f"<p><a href=\"bye?name=Alex\">bye?name=Alex</a></p>"
    body += f"<p><a href=\"planet_distances\">planet_distances</a></p>"
    body += f"<p><a href=\"foobar\">foobar</a></p>"
    return body

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

@app.route('/foobar')
def foobar():
    name = request.args.get('name', 'Alex')
    data = {
    "name": name,
    "city": "Doggerland"
    }

    # Convert dictionary to JSON string
    json_data = json.dumps(data)
    return json_data

if __name__ == '__main__':
    app.run(debug=True, port=8888)