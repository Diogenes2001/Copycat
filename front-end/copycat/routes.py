from flask import render_template, url_for, request, redirect
from copycat import app
from copycat.forms import nameForm, timeForm
import random



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
    time_options = ["30 sec", '40 sec', '50 sec', '60 sec']
    return render_template('settings.html', name=name, random_number=random_number, times=time_options)

@app.route("/game", methods=['GET', 'POST'])
def game():
    session = request.args.get('session')
    time = request.args.get('round_time')
    return render_template('gamesession.html',session_number=session, round_time=time)
