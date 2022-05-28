from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'HELLO WORLD'


if __name__ == '__main__': \
        app.run(debug=True, host='0.0.0.0')
