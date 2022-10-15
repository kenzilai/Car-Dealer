from flask_app import app, bcrypt
from flask_app.models.model_user import User
from flask_app.models.model_car import Car
from flask import render_template, request, redirect, session, flash

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/dashboard')
def show_all_cars():
    if 'user_id' not in session:
        return redirect('/')
    all_car = Car.get_all_cars()
    return render_template('dashboard.html', cars = all_car)

@app.route('/new')
def new_car():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new.html')

@app.route('/add', methods=['POST'])
def add_car():
    if not Car.validation_new(request.form):
        return redirect('/new')
    car_data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make' : request.form['make'],
        'year' : request.form['year'],
        'description' : request.form['description'],
        'user_id': session['user_id']
    }
    Car.add_car(car_data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_car_by_id(id):
    if 'user_id' not in session:
        return redirect('/')
    car_data = {
        'id': id
    }
    car = Car.view_car(car_data)
    return render_template('edit.html', car = car)

@app.route('/update/<int:id>', methods=['POST'])
def update_car(id):
    if not Car.validation_new(request.form):
        return redirect(f'/edit/{id}')
    car_data = {
        'id': id,
        'price': request.form['price'],
        'model': request.form['model'],
        'make' : request.form['make'],
        'year' : request.form['year'],
        'description' : request.form['description'],
        'user_id': session['user_id']
    }
    Car.update_car(car_data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/')
    car_data = {
        'id': id
    }
    return render_template('show.html', car = Car.view_car(car_data))

@app.route('/delete/<int:id>')
def delete_car(id):
    car_data = {
        'id': id
    }
    Car.delete_car(car_data)
    return redirect('/dashboard')