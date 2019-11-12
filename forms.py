from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import Required, Length, InputRequired


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[InputRequired('La contraseña es requerida'),Length(min=5,message='Deben ser mas de 5 caracteres')])
    enviar = SubmitField('Ingresar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()]) #se hereda la el campo de pass y se agrgea el campo de verificacion
    enviar = SubmitField('Registrarse')


'''
FORMS.PY
from flask_wtf import RecaptchaField
recaptcha= RecaptchaField()

APP.PY 
app.config['RECAPTCHA_PUBLIC_KEY']= 'SARAZA'

REGISTRAR.HTML
form.recaptcha


'''