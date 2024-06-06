from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Form for logging in"""
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Login")


class CreateAccountForm(FlaskForm):
    """Form for creating an account"""
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Create Account")
