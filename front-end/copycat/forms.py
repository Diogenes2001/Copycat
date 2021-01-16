from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class nameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder": "Enter your name"})
    submitNew = SubmitField('New Game', id="new")
    submitJoin = SubmitField('Join Game', id="join")

class timeForm(FlaskForm):
    time_options =["30sec", '40 sec', '50 sec', '60 sec']
    time = SelectField("round_time", validators=[DataRequired()], choices=[(i, i) for i in time_options])
    submitSettings = SubmitField('Start Game')