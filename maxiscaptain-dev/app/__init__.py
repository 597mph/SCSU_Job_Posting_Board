from flask_mail import Mail, Message
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

import os 
from os import environ
import mysql.connector 

load_dotenv('.flaskenv')

IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'csc330'
bootstrap = Bootstrap(app)
moment = Moment(app)

DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_APP_PASSWORD = os.environ.get('MAIL_APP_PASSWORD')
MAIL_SENDER_NAME = os.environ.get('MAIL_SENDER_NAME')

app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = MAIL_USERNAME,
        MAIL_PASSWORD = MAIL_APP_PASSWORD,
        MAIL_DEFAULT_SENDER = (MAIL_SENDER_NAME, MAIL_USERNAME),
        SECRET_KEY = 'some secret key for CSRF')

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
from app.models import User, Applicant
db.create_all()

user = User.query.filter_by(role='Admin').first()
if user is None:
    user_admin = User(username='admin', role='Admin')
    user_admin.set_password('admin')
    db.session.add(user_admin)
    db.session.commit()

user = User.query.filter_by(role='Student').first()
if user is None:
    user_student = User(username='student', role='Student')
    user_student.set_password('student')
    db.session.add(user_student)
    db.session.commit()

user = User.query.filter_by(role='Faculty').first()
if user is None:
    user_faculty = User(username='faculty', role='Faculty')
    user_faculty.set_password('faculty')
    db.session.add(user_faculty)
    db.session.commit()

user = User.query.filter_by(role='Employer').first()
if user is None:
    user_employer = User(username='employer', role='Employer')
    user_employer.set_password('employer')
    db.session.add(user_employer)
    db.session.commit()