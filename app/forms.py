
from  flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegistrationForm(FlaskForm):
    user_Id=StringField('Enter National ID',validators=[DataRequired(),Length(min=8)])
    payment_code=StringField('Enter Mpesa Transaction Code',validators=[DataRequired(),Length(min=10,max=10)])
    firstName=StringField('Firstname',validators=[DataRequired(),Length(max=20)])
    lastName=StringField('Lastname',validators=[DataRequired(),Length(max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    confirm_email = StringField('Confirm Email', validators=[DataRequired(),EqualTo('email')])
    phone_no=StringField('Mobile Number',validators=[DataRequired(),Length(max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')


class LoginForm(FlaskForm):
    user_Id=StringField('Enter National ID',validators=[DataRequired(),Length(min=8,max=8)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Log In')




































































