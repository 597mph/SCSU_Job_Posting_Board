from app import db, login
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64), unique=False)
    password_hash = db.Column(db.String(256), unique=False)
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(64), unique=False)
    title = db.Column(db.String(64), unique=False)
    phone = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=False)
    text = db.Column(db.String(64), unique=False)
    datetime = db.Column(db.String(64), unique=True)
    applicant = db.Column(db.String(64), unique=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'title': self.title,
            'phone': self.phone,
            'email': self.email,
            'text': self.text,
            'datetime': self.datetime}

class Applicant(db.Model):
    __tablename__ = 'applicant'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(64), unique=False)
    entry_id = db.Column(db.Integer, unique=False)
    entry_text = db.Column(db.String, unique=False)
    employer_id = db.Column(db.Integer, unique=False)
    first = db.Column(db.String(64), unique=False)
    last = db.Column(db.String(64), unique=False)

class ApplicationAccept(db.Model):
    __tablename__ = "accept"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(64), unique=False)
    entry_id = db.Column(db.Integer, unique=False)
    entry_text = db.Column(db.String, unique=False)
    employer_id = db.Column(db.Integer, unique=False)
    first = db.Column(db.String(64), unique=False)
    last = db.Column(db.String(64), unique=False)
    
class StudentProfile(db.Model):
    __tablename__ = 'StudentProfile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(64), unique=False)
    first = db.Column(db.String(64), unique=False)
    last = db.Column(db.String(64), unique=False)
    address = db.Column(db.String(64), unique=False)
    phone = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    school = db.Column(db.String(64), unique=False)
    major = db.Column(db.String(64), unique=False)
    grade = db.Column(db.String(64), unique=False)

    def to_dict(self):
        return {
            'first': self.first,
            'last': self.last,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'school': self.school,
            'major': self.major,
            'grade': self.grade}

class FacultyProfile(db.Model):
    __tablename__ = 'FacultyProfile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(64), unique=False)
    first = db.Column(db.String(64), unique=False)
    last = db.Column(db.String(64), unique=False)
    address = db.Column(db.String(64), unique=False)
    phone = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    school = db.Column(db.String(64), unique=False)
    department = db.Column(db.String(64), unique=False)
    office = db.Column(db.String(64), unique=False)

    def to_dict(self):
        return {
            'first': self.first,
            'last': self.last,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'school': self.school,
            'department': self.department,
            'office': self.office}

class EmployerProfile(db.Model):
    __tablename__ = 'EmployerProfile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(64), unique=False)
    first = db.Column(db.String(64), unique=False)
    last = db.Column(db.String(64), unique=False)
    title = db.Column(db.String(64), unique=False)
    organization = db.Column(db.String(64), unique=False)
    address = db.Column(db.String(64), unique=False)
    phone = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    expertise = db.Column(db.String(64), unique=False)
    
    def to_dict(self):
        return {
            'first': self.first,
            'last': self.last,
            'title': self.title,
            'organization': self.organization,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'expertise': self.expertise}

@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))