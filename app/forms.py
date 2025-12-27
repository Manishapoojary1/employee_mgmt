from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Register')

class EmployeeForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    department = StringField('Department', validators=[Optional()])
    position = StringField('Position', validators=[Optional()])
    salary = FloatField('Salary', validators=[Optional()])
    date_joined = DateField('Date joined', validators=[Optional()])
    submit = SubmitField('Save')
