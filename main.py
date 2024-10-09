#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'Alex')
    return f"Hello {name}!"

@app.route('/bye')
def bye():
    name = request.args.get('name', 'Alex')
    return f"Goodbye {name}!"

if __name__ == '__main__':
    app.run(debug=True)