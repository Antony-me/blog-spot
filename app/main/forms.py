from wtforms.validators import Required, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField, TextAreaField, SelectField, validators 
from flask_wtf import FlaskForm


class PostForm(FlaskForm):

    title = StringField('post title',validators=[Required()])
    text = TextAreaField('Text',validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment:',validators=[Required()])
    submit = SubmitField('Submit')



class LoginForm(FlaskForm):
  
    email = StringField('Email', validators=[Required()])

    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me?')
    

    submit = SubmitField('Login Up')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class AddPost(FlaskForm):
    title = StringField('post title',validators=[Required()])
    content = TextAreaField('Your post.',validators = [Required()])
    submit = SubmitField('Submit')

