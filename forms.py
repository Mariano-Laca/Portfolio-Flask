#Importar

from flask_wtf import FlaskForm
#Aquí importamos, campodetexto, validadoresdedatos, y el boton submit
from wtforms import StringField, validators, SubmitField
#Aquí de los validadores importamos el datoobligatorio y el email
from wtforms.validators import DataRequired, Email
import email_validator

class miformulario(FlaskForm):
    name = StringField(label='Nombre', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = StringField(label='Mensaje')
    submit = SubmitField(label="Enviar")

