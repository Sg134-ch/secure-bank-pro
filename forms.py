from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TransferForm(FlaskForm):
    recipient_email = StringField('Recipient Email', validators=[DataRequired(), Email()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be positive.")])
    submit = SubmitField('Secure Transfer')
    
    def validate_recipient_email(self, recipient_email):
        user = User.query.filter_by(email=recipient_email.data).first()
        if not user:
            raise ValidationError('Recipient not found in our secure network.')

class AdminDepositForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be positive")])
    submit = SubmitField('Deposit')

class BillPayForm(FlaskForm):
    biller = SelectField('Select Biller', choices=[('BESCOM (Electricity)', 'BESCOM (Electricity)'), ('BWSSB (Water)', 'BWSSB (Water)'), ('Jio Fiber', 'Jio Fiber'), ('HDFC Credit Card', 'HDFC Credit Card')])
    account_number = StringField('Biller Account Number', validators=[DataRequired(), Length(min=5, max=20)])
    amount = FloatField('Payment Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Payment must be greater than 0.")])
    submit = SubmitField('Pay Bill Securely')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters for security.")])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message="Passwords must match.")])
    submit = SubmitField('Update Password')
