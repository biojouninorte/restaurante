import os
import sqlite3
from datetime import datetime, date
from flask import Flask, request, render_template, flash, jsonify, redirect
from sqlite3 import Error
from db import sqlconnection
import usuario_controller
import bebida_controller

app = Flask(__name__)
app.secret_key=os.urandom(24)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/about', methods=["GET"])
def about():
    return render_template('Acerca-de.html')

@app.route('/bebidas', methods=["GET"])
def getBebidas():
    if request.method == 'GET':
        return render_template('bebidas_list.html', row = bebida_controller.list_bebidas())       
     
@app.route('/contacto', methods=["GET","POST"])
def contacto():
    return render_template('contacto.html')

@app.route('/detalle_plato', methods=["GET"])
def detalle_plato():
    return render_template('detalle_plato.html')

@app.route('/register', methods=["GET","POST"])
def register():
    try:
        if request.method == 'POST':
            print("Entro al POST")
            error = None
            password = request.form['password']
            email = request.form['email']

            nombre = request.form['nombre']
            apellido = request.form['apellido']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            created_by = date.today()
            updated_by = date.today()
            print("Validar usuario por email: ", created_by, updated_by)
            comprobar = usuario_controller.get_validarusuario(email)
            print("Comprobación", comprobar)
            if comprobar is not None:
                error = "El correo ya existe".format(email)
                flash(error)
                return render_template('registro.html')
            
            crear = usuario_controller.insert_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by)
            print("ESTA AQUi", crear)
            return redirect('menu')
        return render_template('registro.html')
    except:

        return render_template('registro.html')
    

@app.route('/login', methods=["GET","POST"])
def login():
    return render_template('inicio_sesion.html')

@app.route('/menu', methods=["GET"])
def getMenu():
    return render_template('menu_list.html')

@app.route('/usuarios', methods=["GET", "POST"])
def getUsuarios():
    
    if request.method == 'GET':
        usuario_list = usuario_controller.get_usuarios()
        return render_template('usuarios_list.html', usuario_list=usuario_list)
    

@app.route('/update_user', methods=["GET","POST"])
def update_user():
    return render_template('usuario_update_form.html')

@app.route('/update_bebida', methods=["GET","POST"])
def update_bebida():
    return render_template('bebida_update_form.html')

@app.route('/busqueda', methods=["GET"])
def busqueda():
    return render_template('busqueda.html')

@app.route('/favoritos', methods=["GET"])
def favoritos():
    return render_template('favoritos.html')

@app.route('/compra', methods=["GET"])
def compra():
    return render_template('compra.html')

@app.route('/addBebida', methods=["GET","POST"])
def agregar_bebida():
    return render_template('addBebida.html')


if __name__ =='__main__':
    app.run(debug=True)


##
