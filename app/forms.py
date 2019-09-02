from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, DateTimeField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional
from datetime import datetime, date

def plausible_bf(form, field):
    if field.data:
        print('BF processed',flush=True)
        if field.data > 40:
            raise ValidationError('BF% is too high. Should be < 40%')
        if field.data < 8:
            raise ValidationError('BF% is too low. Should be > 8%')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')
    
class WeighInForm(FlaskForm):
    weight = DecimalField(label='Weight', validators=[DataRequired()])
    bf = DecimalField(label='Body Fat %', validators=[Optional(),plausible_bf])
    wdate = DateField(
        label='Date',
        format='%d-%m-%Y',
        validators=[DataRequired()],
        default=datetime.today().date
    )
    wtime = DateTimeField(
        label='Time',
        format='%H:%M:%S',
        validators=[DataRequired()],
        default=datetime.today().time
    )
    submit = SubmitField('Save')