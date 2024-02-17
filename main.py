import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, session, request
from checker import check_logged_in

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config['dbconfig'] = os.getenv("sql_config")

@app.route('/')
def home_page():
    return render_template('home.html', the_title='Welcome to the Mata Forum Page!')

@app.route('/secret')
@check_logged_in
def secret_page():
    return "if you are seeing this then you are logged in!"

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    session['logged_in'] = True

    return render_template('login.html', msg='')

@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    return 'You have logged out'

app.secret_key = os.getenv("secret_key")

if __name__ == "__main__":
    app.run(debug=True)