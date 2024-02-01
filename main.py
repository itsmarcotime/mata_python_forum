from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('entry.html', the_title='Welcome to the Mata Forum Page!')

@app.route('/login')
def login_page():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)