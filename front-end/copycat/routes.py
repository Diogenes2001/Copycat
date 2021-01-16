from flask import render_template, url_for, request
from copycat import app
from copycat.forms import nameForm
import random


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html", form=nameForm())

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    random_number = random.randint(1, 10000000)
    name = request.args.get('name_input')
    times = ['30 sec','40 sec','50 sec','60 sec']
    return render_template('settings.html', name=name, random_number=random_number, times=times)

@app.route("/game", methods=['GET', 'POST'])
def game():
    session = request.args.get('session')
    return render_template('gamesession.html')