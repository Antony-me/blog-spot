from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegistrationForm, LoginForm
from . import auth
from ..import db
from ..models import User
# from ..email import mail_message


# registration route
@auth.route('/reqister',methods=['GET','POST'])
def register():
    """
    Function that registers the users
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account succesfully created!!', 'success')
        
        
        return redirect(url_for('auth.login'))

    title = "Registration"

    

    return render_template('auth/register.html', form = form, title = title)

# Login function
@auth.route('/login',methods=['GET','POST'])
def login():
    """
    Function that checks if the form is validated
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):

            flash(f'Welcome, You are signed in as {form.username.data}!', 'success')

            login_user(user,form.remember.data)

            return redirect(request.args.get('next') or url_for('main.home'))
        else:
    
            flash('Invalid Username or Password', 'danger')

    return render_template('auth/login.html', form = form)


#logout function
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))