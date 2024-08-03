from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import Company
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    company_id = SelectField('Company', coerce=int)
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Log In')

class UploadForm(FlaskForm):
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    document_file = FileField('Document', validators=[DataRequired()])
    submit = SubmitField('Upload')
