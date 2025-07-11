from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class AnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    species = SelectField('Species', choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
    city = StringField('City', validators=[DataRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    contact = StringField('Contact Info', validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField('Submit')
