#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    trocola = request.args.get('name', 'Mundo')
    return f"¡Hola {trocola}!"

if __name__ == '__main__':
    app.run(debug=True)