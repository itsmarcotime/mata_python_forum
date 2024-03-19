from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Helloworld"

    from .main_pages import main_pages
    from .auth_pages import auth_pages

    app.register_blueprint(main_pages, url_prefix="/")
    app.register_blueprint(auth_pages, url_prefix="/")

    return app


