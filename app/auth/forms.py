from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required,Email,EqualTo, ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[Required()])

    email = StringField('Email', validators=[Required()])

    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators =[Required(), EqualTo('password')])

    submit = SubmitField('sign Up')
    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')


class LoginForm(FlaskForm):
  
    username = StringField('Username', validators=[Required()])

    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me?')
    

    submit = SubmitField('Login In')

