import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for
from checker import check_logged_in
import mysql.connector, hashlib, re

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)

dbconfig = {
    'host': os.getenv("sql_config_host"),
    'user': os.getenv("sql_config_user"),
    'password': os.getenv("sql_config_password"),
    'database': os.getenv("sql_config_database")
}
conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()

@app.route('/')
def base_page():
    return render_template('base.html', the_title='Welcome to the Mata Forum Page!')

@app.route('/home')
@check_logged_in
def home():
    return render_template('home.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def do_register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # check if account exists in mysql
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # if account exists show error && validation checks
        if account:
            msg = 'This account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'You did not use a correct email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Sorry, Username can only contain characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out all the feilds in the form!'
        else:
            # Need to hash password
            # Account doesnt exits && the form is filled out so creat the user
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            conn.commit()
            msg = 'You have successfully registered your account! Continue to login.'

    elif request.method == 'POST':
        msg = 'Please fill out the required fields.'

    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM accounts WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchone()

        if record:
            session['logged_in'] = True
            session['username'] = record[1]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username or password. Try again!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    session.pop('username')
    return redirect(url_for('do_login'))

@app.route('/add_post', methods=['GET', 'POST'])
@check_logged_in
def add_post():
    msg = ''

    if request.method == 'POST' and 'title' in request.form and 'body' in request.form:
        title = request.form['title']
        body = request.form['body']
        cursor.execute('INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)', (title, body, session['username']))
        conn.commit()
        msg = 'Your post was created successfully!'
        return redirect(url_for(home))
    
    return render_template('add_post.html', msg=msg)

    



app.secret_key = os.getenv("secret_key")

if __name__ == "__main__":
    app.run(debug=True)