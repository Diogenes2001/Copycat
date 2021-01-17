from flask import render_template, url_for, request, redirect
from frontend import app
from frontend.forms import nameForm, joinForm
from opentok import OutputModes
import random
from frontend.__init__ import api_key, session, opentok, the_game

archiveID = "super secret"
nameDict = []
current = 0
nameDictionary = {}

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = nameForm()
    if form.validate_on_submit():
        if form.submitNew.data:
            return redirect(url_for('settings', name_input=form.name.data))
        if form.submitJoin.data:
            return redirect(url_for('join', name_input=form.name.data))
    return render_template("home.html", form=form)

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    global nameDict
    random_number = random.randint(1, 10000000)
    name = request.args.get('name_input')
    return render_template('settings.html', name=name, random_number=random_number,)

@app.route("/game", methods=['GET', 'POST'])
def game():
    key = api_key
    global session_id
    session_id = session.session_id
    token = opentok.generate_token(session_id)
    sessionNr = request.args.get('session')
    name = request.args.get('name')
    nameDict.append(name)
    return render_template('gamesession.html', name=name,session_number=sessionNr, api_key=key, session_id=session_id, token=token)

@app.route('/background_process')
def background_process():
    global archiveID
    global current
    print ("Hello")
    print(archiveID)
    if (archiveID != "super secret"):
        opentok.stop_archive(archiveID)
        archive = opentok.get_archive(archiveID)
        while (archive.status != "available"):
            print(archive.status)
            archive = opentok.get_archive(archiveID)
        filename = nameDictionary[nameDict[current]] + '.webm'
        print(filename)
        the_game.process_video(archive.url, filename)
        current = current + 1
        if (current >= len(nameDict)):
            current = 0
    else:
        nameDict.sort()
    archive = opentok.start_archive(session_id, output_mode=OutputModes.individual)
    print(nameDict[current])
    archiveID = archive.id
    return { "players": nameDict }

@app.route('/background_process_addname')
def background_process_addname():
    global nameDictionary
    global current
    name = request.args.get('name')
    streamid = request.args.get('id')
    nameDictionary[name] = streamid
    print(nameDictionary)
    return nameDict[current]

@app.route('/join')
def join():
    form = joinForm()
    name = request.args.get('name_input')
    if form.validate_on_submit():
        return redirect(url_for('game'))
    return render_template('join.html', form=form, name=name)