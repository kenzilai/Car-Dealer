from flask_app import app, bcrypt
from flask_app.models.user_model import User
from flask_app.models.car_model import Car
from flask import render_template, request, redirect, session, flash

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validation_register(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    new_user = User.register(data)
    session['user_id'] = new_user
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login_user():
    if not User.validation_login(request.form):
        return redirect('/')
    user = User.get_by_email(request.form)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')