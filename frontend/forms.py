from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class nameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder": "Enter your name"})
    submitNew = SubmitField('New Game', id="new")
    submitJoin = SubmitField('Join Game', id="join")

class joinForm(FlaskForm):
    session = StringField('session', validators=[DataRequired(), Length(min=2, max=20)],
                       render_kw={"placeholder": "Enter the game session code"})
    submitJoinSession = SubmitField('Join Session', id='joinsession')

