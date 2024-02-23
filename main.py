import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for
from checker import check_logged_in
import mysql.connector

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
# @check_logged_in
def home():
    return render_template('home.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def do_register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
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

app.secret_key = os.getenv("secret_key")

if __name__ == "__main__":
    app.run(debug=True)