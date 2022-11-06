from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self,data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.password = data['password']
        # add other values, fname, lname, email,
        #  password

        # sensei bonus idea: age, validation
        # but be >60, grandpas only dating site

    @classmethod
    def save(cls, data):
        query ='''INSERT INTO users (fname, lname, email, password) 
        VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);'''
        return connectToMySQL('grandpasonly').query_db(query,data)


    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['fname']) < 1:
            flash("First Name cannot be blank")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if user['password'] != user['confirm']:
            flash('passwords must match')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("grandpasonly").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def getOne(cls,data):
        query = '''
        SELECT * FROM users
        WHERE id = %(id)s;'''
        result = connectToMySQL('grandpasonly').query_db(query,data)
        return cls(result[0])
    


#bcrypt code
# bcrypt.generate_password_hash(password_string)
# compare
# bcrypt.check_password_hash(hashed_password, password_string)
# Bcrypt Notes:
#  If we pass it a string and print the result, we may see something like this:

# $2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC
# We will store this string in our database, 
# and there is a lot of information contained in it! 
# Within the first set of $ signs, 
# we have the Bcrypt ID (in this case, 2b). 
# Between the next set of $ signs, 
# the number 12 tells us how many rounds of hashing we did - 
# this is what slows Bcrypt down. 
# The next 22 characters is the salt (128 bits), and the rest is our 184-bit hash.
