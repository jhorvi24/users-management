from users_app.models import Users
from users_app import app, db, login_manager
from users_app.forms import RegisterForm, LoginForm
from flask import request, make_response, flash, redirect, url_for, render_template, session
from flask_login import login_user, logout_user, login_required, current_user
from flask import jsonify

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        created_user = Users(username=form.username.data, 
                             password_hash=form.password1.data, 
                             email=form.email.data)
        print(type(created_user))
        db.session.add(created_user)
        db.session.commit()
        login_user(created_user)
        
        flash('User created successfully! You are now logged in as {create_user.username}', category='success')
        #return redirect(url_for('catalog'))
        return jsonify({'message': 'User created successfully! You are now logged in as {create_user.username}'}), 201
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)
    
@app.route('/register/<username>/validate')
def validate_username(username):
    print("validate the user")
    print(username)
    #validate if the user is in databases
    user = Users.query.filter_by(username=username).first()
    if user is not None:
        response = jsonify({'message': 'True'})
    else:
        response = jsonify({'message': 'Cannot find username'}), 404
    return response

@app.route('/register/<email>/validatemail')
def validate_email(email):
    print("Validate the email")
    #validate if the email is in databases
    
    email = Users.query.filter_by(email=email).first()
    
    if email is not None:
        response = jsonify({'message': 'True'})
    else:
        response = jsonify({'message': 'Cannot find email'}), 404
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():    
    
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form.username.data).first()
        print(attempted_user)
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('catalog'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)   
     
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    #return redirect(url_for('home'))
    
    return jsonify({'message': 'You have been logged out!'}), 200
    