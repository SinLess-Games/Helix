# imports
from flask import Flask, render_template, request, redirect, url_for, flash

# flask server initialization
app = Flask(__name__)
app.secret_key = 'secret'

# define flask server run
async def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=True)

async def stop_flask():
    app.stop()

# Routes for flask server
@app.route('/')
def home():
    return render_template('html/home.html')

@app.route('/about')
def about():
    return render_template('html/about.html')