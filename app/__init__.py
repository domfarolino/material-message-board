from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config.from_pyfile('config.py')

api = Api(app)
db = SQLAlchemy(app)
lm = LoginManager(app)

lm.login_view = 'index'

from app import views
from app import models