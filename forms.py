from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()]) #se hereda la el campo de pass y se agrgea el campo de verificacion
    enviar = SubmitField('Registrarse')
