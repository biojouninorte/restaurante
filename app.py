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

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/register')
def register():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('inicio_sesion.html')

@app.route('/menu')
def getMenu():
    return render_template('menu_list.html')

@app.route('/bebidas')
def getBebidas():
    return render_template('bebidas_list.html')




if __name__ =='__main__':
    app.run(debug=True)


##