from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, RadioField, EmailField, TextAreaField 
from wtforms.validators import DataRequired, Email
from email_validator import validate_email

class AddUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    grade_level = StringField('Grade Level', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class DeleteForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Delete')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordRetype = PasswordField('Retype Password', validators=[DataRequired()])
    accountType = RadioField('Account Type', choices=(('Student'),('Faculty'),('Employer')))
    submit = SubmitField('Create Account')

class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Old Password', validators=[DataRequired()])
    new_pass = PasswordField('New Password', validators=[DataRequired()])
    new_pass_retype = PasswordField('Retype New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    business = StringField('Company Name', validators=[DataRequired()])
    contact = StringField('Hiring Manager', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Share')

class StudentProfileForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()]) 
    last = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    grade = StringField('Grade', validators=[DataRequired()])
    submit = SubmitField('Update Profile', validators=[DataRequired()])

class FacultyProfileForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()]) 
    last = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    office = StringField('Office', validators=[DataRequired()])
    submit = SubmitField('Update Profile', validators=[DataRequired()])

class EmployerProfileForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()]) 
    last = StringField('Last Name', validators=[DataRequired()])
    business_name = StringField('Organization', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    expertise = StringField('Expertise', validators=[DataRequired()])
    submit = SubmitField('Update Profile', validators=[DataRequired()])

#create a search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

#creates male 
class MailForm(FlaskForm):
    email = StringField('Recipient: ', validators=[DataRequired()])
    message = TextAreaField('Your message:', validators=[DataRequired()])
    submit = SubmitField('Send')

