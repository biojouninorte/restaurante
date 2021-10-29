import os
import sqlite3
import smtplib
from decouple import config as config_decouple
import pandas as pd
from datetime import datetime, date
from flask import Flask, url_for, request, render_template, flash, jsonify, redirect, session
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph
from sqlite3 import Error
from db import sqlconnection
import usuario_controller
import bebida_controller
import pedido_controller
import favoritos_controller

from formulario import BebidaForm

app = Flask(__name__)
PORT = 5000
DEBUG = False
app.secret_key=os.urandom(24)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/about', methods=["GET"])
def about():
    return render_template('Acerca-de.html')    
     
@app.route('/contacto', methods=["GET","POST"])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        mensaje = request.form['mensaje']
        res = pd.DataFrame({'Nombre':nombre, 'email':email, 'telefono':telefono ,'mensaje':mensaje}, index=[False])
        res.to_csv('./Mensajecontacto.csv', mode='a',index=False, header=False)
        print("Los datos fueron enviados !")
        respuesta = "Gracias por contactarnos, en el transcurso del dia estaremos respondiendo a tu solicitud"
        try:
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("juiceitup50@gmail.com","uniNORTE50*") # correo creado gmail
            server.sendmail("juiceitup50@gmail.com",email,respuesta)
            print("Mensaje enviado !")
            return render_template('contacto.html')
        except:
            print("error enviando")
    else:
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
            hash_clave = checkph(user["password"], password)
            if user != None and hash_clave == True:
                session["id"] = user["id"]
                session["email"] = user["email"]
                session["nombre"] = str(user["nombre"]) +" "+str(user["apellido"])
                session["super"] = user["superAdmin"]
                session["admin"] = user["admin"]
                session["cliente"] = user["usuarioFinal"]
                session["telefono"] = user["telefono"]
                session["direccion"] = user["direccion"]
                session["bebida"] = []
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
    if session:
        #session.pop("usuario", None)    
        session.clear()
        return redirect(url_for("login"))

    else:
        return '<p> El usuario ya ha cerrado la sesión. <a href="/login">Login</a></p>'

@app.route('/menu', methods=["GET"])
def getMenu():
    
    if session:
        row = bebida_controller.get_bebidas()
        return render_template('menu_list.html', row = row)
    return redirect(url_for("login"))

@app.route('/usuarios', methods=["GET", "POST"])
def getUsuarios():
    if session:
        if request.method == 'GET':
            if session["super"] == 1 or session["admin"] == 1:
                usuario_list = usuario_controller.get_usuarios()
            else:
                id = session["id"] 
                usuario_list = usuario_controller.get_usuario(id)
            return render_template('usuarios_list.html', usuario_list=usuario_list)
    return redirect(url_for("login"))
    

@app.route('/update_user/<int:id>', methods=["GET","POST"])
def update_user(id):
    if session:
        try:
            if request.method == 'POST':
                nombre = request.form['nombre']
                apellido = request.form['apellido']
                email = request.form['email']
                telefono = request.form['telefono']
                direccion = request.form['direccion']
                password = genph(request.form['new_password'])
                created_by = date.today()
                updated_by = date.today()
                crear = usuario_controller.update_usuario(nombre,apellido,email,telefono,direccion,password,created_by,updated_by,id)
                return redirect(url_for("getUsuarios"))
            return render_template('usuario_update_form.html', row = usuario_controller.get_usuario(id))    
        except:
            return render_template('usuario_update_form.html', row = usuario_controller.get_usuario(id))
    return redirect(url_for("login"))

@app.route('/eliminarusuario/<int:id>', methods=["GET"])
def eliminarUsuario(id):
    if session:
        usuario_controller.delete_usuario(id)
    return redirect(url_for("getUsuarios"))

@app.route('/busqueda', methods=["GET"])
def busqueda():
    return render_template('busqueda.html')


#favoritos
@app.route('/favoritos', methods=["GET"])
def favoritos():
    if session:
        if request.method == 'GET':
            usuario_id = session["id"]
            return render_template('favoritos.html', row = favoritos_controller.get_favoritos(usuario_id))
        
    return redirect(url_for("login"))
        

@app.route('/eliminarfavorito/<int:id>', methods=["GET"])
def eliminarFavorito(id):
    if session:
        favoritos_controller.delete_favorito(id)
    return redirect(url_for("favoritos"))

@app.route('/agregarfavorito/<int:id>', methods=["GET", "POST"])
def agregarFavorito(id):
    if session:
        if request.method == 'POST':
            usuario_id = session["id"]
            bebida_id = id
            favoritos_controller.agregar_favoritos(bebida_id, usuario_id)
            return redirect(url_for("favoritos"))
    return redirect(url_for("login"))

# Pedidos 
@app.route('/compra', methods=["GET", "POST"])
def compra():
    if session:
        listado = []
        for id in session["bebida"]:
            dict_pedido = {}
            row = bebida_controller.get_bebida(id)
            
            dict_pedido["id"] = row["id"]
            dict_pedido["nombre"] = row["nombreBebida"]
            dict_pedido["precio"] = row["precio"]
            listado.append(dict_pedido)

        if request.method == "POST":
            usuario_id = session["id"]
            created_by = date.today()
            updated_by = date.today()
            direccion = session["direccion"]

            for instance in listado:
                bebida_id = instance["id"]
                indicador = "numero"+str(bebida_id)
                valor = int(request.form[indicador])

                add = pedido_controller.insert_pedido(usuario_id, bebida_id, valor, direccion, created_by, updated_by)

            return redirect(url_for(getMenu))

        return render_template('compra.html', row = listado)
    return redirect(url_for("login"))

@app.route('/agregar-pedido/<int:id>', methods=["POST"])
def addPedido(id):
    if session:
        lista = session["bebida"]
        if request.method == 'POST':
            lista.append(id)
            session["bebida"] = lista
            
            return redirect(url_for("compra"))
    return redirect(url_for("login"))

#favoritos
@app.route('/listado-pedidos', methods=["GET"])
def listPedidos():
    if session:
        if request.method == 'GET':
            
            pedidos = pedido_controller.get_pedidos()
            usuarios = usuario_controller.get_usuarios()
            bebidas = bebida_controller.get_bebidas()
            
            return render_template('pedidos_list.html', pedidos = pedidos, usuarios = usuarios, bebidas = bebidas)
        
    return redirect(url_for("login"))


# Bebidas

@app.route('/bebidas', methods=["GET"])
def getBebidas():
    if session:
        if request.method == 'GET':
            if session["super"] == 1 or session["admin"] == 1: 
                return render_template('bebidas_list.html', row = bebida_controller.get_bebidas())  
            return redirect(url_for("getMenu"))
    return redirect(url_for("login"))


@app.route('/addBebida', methods=["GET","POST"])
def agregar_bebida():
    if session:
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
    if session:
        bebida_controller.delete_bebidas(id)
    return redirect(url_for("getBebidas"))

@app.route('/update_bebida/<int:id>', methods=["GET","POST"])
def update_bebida(id):
    if session:
        try:
            if request.method == 'POST':         
                nombre = request.form['nombre']
                descripcion = request.form['descripcion']
                precio = request.form['precio']
                disponibilidad = request.form['disponibilidad']
                crear = bebida_controller.update_bebida(nombre,descripcion,precio,disponibilidad,id)
                return redirect(url_for("getBebidas"))
            return render_template('bebida_update_form.html', row = bebida_controller.get_bebida(id))
        except:
            return render_template('bebida_update_form.html', row = bebida_controller.get_bebida(id))
    return redirect(url_for("login"))


@app.route('/detalle_plato/<int:id>/', methods=["GET", "POST"])
def detalle_plato(id):
    if session:
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
            usuario_id = session["id"]
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
    app.run(debug=DEBUG)


##
