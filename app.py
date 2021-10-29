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
import favoritos_controller

from formulario import BebidaForm

app = Flask(__name__)
app.secret_key=os.urandom(24)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/about', methods=["GET"])
def about():
    return render_template('Acerca-de.html')    
     
@app.route('/contacto', methods=["GET","POST"])
def contacto():
    return render_template('contacto.html')



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
    try:
        
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
    except:
        return render_template('inicio_sesion.html')

@app.route('/logout')
def logout():
    if "usuario" in session:
        #session.pop("usuario", None)    
        session.clear()
        return redirect(url_for("login"))

    else:
        return '<p> El usuario ya ha cerrado la sesión. <a href="/login">Login</a></p>'

@app.route('/menu', methods=["GET"])
def getMenu():
    if "usuario" in session:
        row = bebida_controller.get_bebidas()
        return render_template('menu_list.html', row = row)
    return redirect(url_for("login"))

@app.route('/usuarios', methods=["GET", "POST"])
def getUsuarios():
    if "usuario" in session:
        if request.method == 'GET':
            usuario_list = usuario_controller.get_usuarios()
            return render_template('usuarios_list.html', usuario_list=usuario_list)
    return redirect(url_for("login"))
    

@app.route('/update_user', methods=["GET","POST"])
def update_user():
    if "usuario" in session:
        if request.method == 'POST':
            pass
        return render_template('usuario_update_form.html')
    return redirect(url_for("login"))

@app.route('/eliminarusuario/<int:id>', methods=["GET"])
def eliminarUsuario(id):
    if "usuario" in session:
        usuario_controller.delete_usuario(id)
    return redirect(url_for("getUsuarios"))

@app.route('/update_bebida', methods=["GET","POST"])
def update_bebida():
    if "usuario" in session:
        if request.method == 'POST':
            pass
        return render_template('bebida_update_form.html')
    return redirect(url_for("login"))

@app.route('/busqueda', methods=["GET"])
def busqueda():
    return render_template('busqueda.html')


#favoritos
@app.route('/favoritos', methods=["GET"])
def favoritos():
    if request.method == 'GET':
        return render_template('favoritos.html', row = favoritos_controller.get_favoritos()) 

@app.route('/eliminarfavorito/<int:id>', methods=["GET"])
def eliminarFavorito(id):
    if "usuario" in session:
        favoritos_controller.delete_favorito(id)
    return redirect(url_for("favoritos"))

@app.route('/agregarfavorito/<int:id>', methods=["GET"])
def agregarFavorito(id):
    if "usuario" in session:
        favoritos_controller.agregar_favoritos(id)
    return redirect(url_for("favoritos"))

@app.route('/compra', methods=["GET"])
def compra():
    return render_template('compra.html')


# Bebidas

@app.route('/bebidas', methods=["GET"])
def getBebidas():
    if request.method == 'GET':
        return render_template('bebidas_list.html', row = bebida_controller.get_bebidas())   

@app.route('/addBebida', methods=["GET","POST"])
def agregar_bebida():
    if "usuario" in session:
        form = BebidaForm()
        if request.method == 'POST':
            nombreBebida = form.nombre.data
            precio = form.precio.data
            descripcion = form.descripcion.data
            activo = form.estado.data
            created_by = date.today()
            updated_by = date.today()
            if activo == True:
                estado = 1
            else:
                estado = 0
            add = bebida_controller.insert_bebida(nombreBebida, descripcion, precio, estado, created_by, updated_by)
            # Con url_for se llama a la función no la ruta.
            return redirect(url_for('getBebidas'))

        return render_template('addBebida.html', form=form)
    return redirect(url_for("login"))

@app.route('/eliminarbebidas/<int:id>', methods=["GET"])
def eliminarBebidas(id):
    if "usuario" in session:
        bebida_controller.delete_bebidas(id)
    return redirect(url_for("getBebidas"))

@app.route('/detalle_plato/<int:id>/', methods=["GET", "POST"])
def detalle_plato(id):
    if "usuario" in session:
        # Bebidas
        row = bebida_controller.get_bebida(id)
        # Calificacion por id de bebidas
        rowCal = bebida_controller.get_calificaciones(id)
        total = 0
        num_registro = 0
        for r in rowCal:
            total += r[0]
            num_registro += 1

        if num_registro > 0:
            promedio = total/num_registro
        else:
            promedio = 0

        # Calificacion por id de bebidas
        comentario = bebida_controller.get_comentarios()

        if request.method == 'POST':
            bebidas_id = id
            usuario_id = session["usuario"][0]
            mensaje = request.form['mensaje']
            created_by = date.today()
            update_by = date.today()
            estrellas = request.form['estrellas']
            add = bebida_controller.comentario_bebida(bebidas_id, usuario_id, mensaje, estrellas, created_by, update_by)
            
            calificarBebida(bebidas_id, estrellas)
       
        return render_template('detalle_plato.html', row = row, estrella = promedio, comentario = comentario)
    return redirect(url_for("login"))

@app.route('/calificar/', methods=["POST"])
def calificarBebida(bebida_id, calificacion):

    add = bebida_controller.calificar_bebida(bebida_id, calificacion)
    return True

if __name__ =='__main__':
    app.run(debug=True)


##
