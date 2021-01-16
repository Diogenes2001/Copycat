from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class nameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder": "Enter your name"})
