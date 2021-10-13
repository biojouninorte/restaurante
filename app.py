import os
from flask import Flask, request, render_template, flash


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
    return render_template('bebidas_list.html')

@app.route('/contacto', methods=["GET","POST"])
def contacto():
    return render_template('contacto.html')

@app.route('/detalle_plato', methods=["GET"])
def detalle_plato():
    return render_template('detalle_plato.html')

@app.route('/register', methods=["GET","POST"])
def register():
    return render_template('registro.html')

@app.route('/login', methods=["GET","POST"])
def login():
    return render_template('inicio_sesion.html')

@app.route('/menu', methods=["GET"])
def getMenu():
    return render_template('menu_list.html')

@app.route('/update_user', methods=["GET","POST"])
def update_user():
    return render_template('usuario_update_form.html')

@app.route('/update_bebida', methods=["GET","POST"])
def update_bebida():
    return render_template('bebida_update_form.html')

@app.route('/usuarios', methods=["GET"])
def getUsuarios():
    return render_template('usuarios_list.html')


if __name__ =='__main__':
    app.run(debug=True)


##
