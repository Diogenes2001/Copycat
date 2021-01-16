from flask import render_template, url_for, request, redirect
from copycat import app
from copycat.forms import nameForm, timeForm
import random
from copycat.__init__ import api_key, session, opentok

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form=nameForm()
    if form.validate_on_submit():
        return redirect(url_for('settings', name_input=form.name.data))
    # elif form.validate_on_submit() and  "Search":
    #     return redirect(url_for('game', name_input=form.name.data))
    return render_template("home.html", form=form)

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    random_number = random.randint(1, 10000000)
    name = request.args.get('name_input')
    return render_template('settings.html', name=name, random_number=random_number)

@app.route("/game", methods=['GET', 'POST'])
def game():
    key = api_key
    session_id = session.session_id
    token = opentok.generate_token(session_id)
    sessionNr = request.args.get('session')
    if request.method == "POST":

        print("it worked")
    return render_template('gamesession.html',session_number=sessionNr, api_key=key, session_id=session_id, token=token)
