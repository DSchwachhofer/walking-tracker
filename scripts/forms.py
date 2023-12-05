from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, length

import datetime

class LoginForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Email(message=("Not a valid email adress"))])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Log In")

class LogWalkForm(FlaskForm):
  date = DateField("Date", validators=[DataRequired()], default=datetime.date.today())
  distance = DecimalField("Distance (km)", validators=[DataRequired()], places=2, default=1)
  time = DecimalField("Duration (min)", validators=[DataRequired()], places=0, default=25)
  submit = SubmitField("Add Walk")