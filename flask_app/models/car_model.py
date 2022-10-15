from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    def __init__(self, car_data):
        self.id = car_data['id']
        self.price = car_data['price']
        self.model = car_data['model']
        self.make = car_data['make']
        self.year = car_data['year']
        self.description = car_data['description'] 
        self.created_at = car_data['created_at']
        self.updated_at = car_data['updated_at']
        self.user_id = car_data['user_id']

    @classmethod
    def get_all_cars(cls):
        query = 'SELECT * FROM car JOIN user ON user.id = car.user_id;'
        results = connectToMySQL(DATABASE).query_db(query)
        show_user_cars = []
        for row in results:
            car = cls(row)
            user_name = {
                **row,
                'first_name': row['first_name'],
                'last_name': row['last_name'],
            }
            car.user = user_name
            show_user_cars.append(car)
        return show_user_cars

    @classmethod
    def get_car_with_user(cls, car_data):
        query = 'SELECT * FROM car JOIN user ON user.id = car.user_id WHERE car.user_id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, car_data)
        show_user_cars = []
        for row in results:
            car = cls(row)
            user_name = {
                **row,
                'first_name': row['first_name'],
                'last_name': row['last_name'],
            }
            car.user = user_name
            show_user_cars.append(car)
        return show_user_cars

    @classmethod
    def view_car(cls, car_data):
        query = 'SELECT * FROM car JOIN user ON user.id = car.user_id WHERE car.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, car_data)
        if results:
            car = cls(results[0])
            for row in results:
                user_name = {
                    **row,
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                }
        car.user = user_name
        return car

    @classmethod
    def add_car(cls, car_data):
        query = 'INSERT INTO car (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s)'
        return connectToMySQL(DATABASE).query_db(query, car_data)

    @classmethod
    def update_car(cls, car_data):
        query = 'UPDATE car SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE id = %(id)s'
        return connectToMySQL(DATABASE).query_db(query, car_data)

    @classmethod
    def delete_car(cls, data):
        query = 'DELETE FROM car WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validation_new(car):
        is_valid = True

        if not car['price']:
            flash('Price must be greater than 0.', "new")
            is_valid = False
        else:
            if int(car['price']) <= 0:
                flash("Price must be greater than 0.", "new")
                is_valid = False
            
        if len(car['model']) <= 0:
            flash("Model must not empty.", "new")
            is_valid = False
            
        if len(car['make']) <= 0:
            flash("Make must not empty", "new")
            is_valid = False

        if car['year']:
            if int(car['year']) <= 0:
                flash("Year must be greater than 0.", "new")
                is_valid = False
        else:
            flash("Year is required.", "new")
            is_valid = False

        if len(car['description']) <= 0:
            flash("Description must not empty.", "new")
            is_valid = False
        
        return is_valid