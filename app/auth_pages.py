from flask import Blueprint, render_template

auth_pages = Blueprint("auth_pages", __name__)

@auth_pages.route('/login')
def login():
    return "login"

@auth_pages.route('/register')
def do_resiter():
    return "register"