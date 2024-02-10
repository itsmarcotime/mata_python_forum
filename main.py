from flask import Flask, render_template, session
from checker import check_logged_in

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html', the_title='Welcome to the Mata Forum Page!')

@app.route('/secret')
@check_logged_in
def secret_page():
    return "if you are seeing this then you are logged in!"

@app.route('/login')
def login_page():
    session['logged_in'] = True
    return "you have logged in!"

@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    return 'You have logged out'

app.secret_key = ''

if __name__ == "__main__":
    app.run(debug=True)