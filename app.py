import os
import sqlite3
from datetime import datetime, date
from flask import Flask, url_for, request, render_template, flash, jsonify, redirect, session

from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph


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
            
            error = None
            password = genph(request.form['password'])
            email = request.form['email']

            nombre = request.form['nombre']
            apellido = request.form['apellido']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            created_by = date.today()
            updated_by = date.today()
            
            #Comprobamos si existe un usuario con el mismo email
            comprobar = usuario_controller.get_validarusuario(email)
           
            if comprobar is not None:
                error = "El correo ya existe".format(email)
                flash(error)
                return render_template('registro.html')
            
            crear = usuario_controller.insert_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by)
            
            return redirect('menu')
        return render_template('registro.html')
    except:

        return render_template('registro.html')
    

@app.route('/login', methods=["GET","POST"])
def login():
    #try:
    if request.method == 'POST':
        
        error = None
        password = request.form['password']
        email = request.form['email']
     
        #Comprobamos si existe un usuario con el mismo email
        user = usuario_controller.get_login(email)
        #Compara las claves ingresadas
        hash_clave = checkph(user[6], password)
        if user != None and hash_clave == True:
            session["usuario"] = user
            return redirect('menu')
        else:
            error = "Usuario o Contraseña inválidos"
            flash(error)
            return render_template('inicio_sesion.html')
            
    return render_template('inicio_sesion.html')
    #except:
        #return render_template('inicio_sesion.html')

@app.route('/logout')
def logout():
    if "usuario" in session:
        #session.pop("usuario", None)    
        session.clear()
        return render_template("login.html")

    else:
        return '<p> El usuario ya ha cerrado la sesión. <a href="/login">Login</a></p>'

@app.route('/menu', methods=["GET"])
def getMenu():
    if "usuario" in session:
        print("Logueado", session["usuario"][3])
        return render_template('menu_list.html')
    else:
        return redirect(url_for("login"))

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
