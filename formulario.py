from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class BebidaForm(FlaskForm):
    nombre=StringField('Nombre', validators=[DataRequired(message='Este campo no puede estar vacío')])
    precio=IntegerField('Precio', validators=[DataRequired(message='Este campo no puede estar vacío')])
    descripcion=StringField('Descripción', validators=[DataRequired(message='Este campo no puede estar vacío')], widget=TextArea())
    estado=BooleanField('Activo', validators=[DataRequired(message='Este campo no puede estar vacío')])

    enviar=SubmitField('Enviar')
    consultar=SubmitField('Consultar')
    listar=SubmitField('Listar')
    actualizar=SubmitField('Actualizar')
    eliminar=SubmitField('Eliminar')