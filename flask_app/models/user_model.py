from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, app, bcrypt
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.email = user_data['email']
        self.password = user_data['password']
        self.created_at = user_data['created_at']
        self.updated_at = user_data['updated_at']

    @classmethod
    def register(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validation_register(user):
        is_valid = True

        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.", "register")
            is_valid = False
            
        if len(user['last_name']) < 3:
                flash("Last Name must be at least 3 characters.", "register")
                is_valid = False
            
        if len(user['email']) < 5:
            flash("Email must be at least 5 characters.", "register")
            is_valid = False
        
        if not EMAIL_REGEX.match(user['email']):
            flash("Email format is incorrect", "register")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        
        if  user['password'] != user['confirm_password']:
            flash("Password is not match.", "register")
            is_valid = False
        
        return is_valid

    @staticmethod
    def validation_login(user):
        is_valid = True
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        result = connectToMySQL(DATABASE).query_db(query, user)
        print(result)

        if len(result) < 1:
            flash("The user does not exist.", "login")
            is_valid = False

        if len(user['password']) < 1:
            flash("Password must be at least 5 characters.", "login")
            is_valid = False

        return is_valid