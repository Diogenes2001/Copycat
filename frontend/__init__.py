from flask import Flask
from opentok import OpenTok, MediaModes
import os
from backend.game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a76d96d18217941ed34797f1733e1cdc'

try:
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]

except Exception:
    raise Exception("You must define API_KEY and API_SECRET environment variables")

opentok = OpenTok(api_key, api_secret)
session = opentok.create_session(media_mode=MediaModes.routed)
the_game = Game()