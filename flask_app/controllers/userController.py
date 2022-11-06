from pydoc import render_doc
from flask_app import app
from flask import redirect, render_template, request, session, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

#old version without hashing
# @app.route('/create/user', methods=['POST'])
# def createUser():
#     if not User.validate_user(request.form):
#         return redirect('/')
#     User.save(request.form)
#     return redirect('/')

#new registration with hashing
@app.route('/create/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_user(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

#home page with logged in user
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect('/welcome')

@app.route('/welcome')
def success():
    if 'user_id' not in session:
        redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.getOne(data)
    return render_template('success.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')