import os
from flask import Flask, request, render_template, flash


app = Flask(__name__)
app.secret_key=os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('Acerca-de.html')

@app.route('/bebidas')
def getBebidas():
    return render_template('bebidas_list.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/detalle_plato')
def detalle_plato():
    return render_template('detalle_plato.html')

@app.route('/register')
def register():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('inicio_sesion.html')

@app.route('/menu')
def getMenu():
    return render_template('menu_list.html')

@app.route('/update_user')
def update_user():
    return render_template('usuario_update_form.html')

@app.route('/update_bebida')
def update_bebida():
    return render_template('bebida_update_form.html')

@app.route('/usuarios')
def getUsuarios():
    return render_template('usuarios_list.html')


if __name__ =='__main__':
    app.run(debug=True)


##