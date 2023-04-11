from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from MapService.models import User
from MapService import users


class RegistraionFrom(FlaskForm):
    username = StringField("Operator name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # validating if username or op_name is already in the database
        user = users.find({"username": {"$eq":username.data}})
        for document in user:
            if document:
                raise ValidationError("This username already exists. Please choose a different username")
    
    def validate_email(self, email):
        # validating if email is already in the database
        user = users.find({"email": {"$eq":email.data}})
        for document in user:
            if document:
                raise ValidationError("This email already exists. Please choose a different email")
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])    
    submit = SubmitField('Update')

    def validate_username(self, username):
        # validating if username or op_name is already in the database
        if username.data != current_user.username:
            user = users.find({"username": {"$eq":username.data}})
            for document in user:
                if document:
                    raise ValidationError("This username already exists. Please choose a different username")
    
    def validate_email(self, email):
        # validating if email is already in the database
        if email.data != current_user.email:
            user = users.find({"email": {"$eq":email.data}})
            for document in user:
                if document:
                    raise ValidationError("This email already exists. Please choose a different email")

