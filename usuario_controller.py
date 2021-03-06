import sqlite3
from flask import Flask
from sqlite3 import Error
from db import sqlconnection, get_db, close_db


# Funciona
def insert_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by):
    #db = sqlconnection()
    try:
        db = get_db()
        #cursor = db.cursor()
        statement = "INSERT INTO usuarios (nombre, apellido, email, telefono, direccion, password, created_by, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        db.execute(statement, (nombre, apellido, email, telefono, direccion, password, created_by, updated_by))
        #db.cursor()
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)
    
    
# Funciona
def update_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by,id):
    #db = sqlconnection()
    try:
        db = get_db()
        statement = "UPDATE usuarios SET nombre = ?, apellido = ? email = ?, telefono = ?, direccion = ?, password = ?, created_by = ?, update_by = ? WHERE id = ?;"
        db.execute("UPDATE usuarios SET nombre=?, apellido=?, email=?, telefono=?, direccion=?, password=? WHERE id = ? ", [nombre, apellido, email, telefono, direccion, password, id])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)

# Funciona
def get_usuario(id):
    db = sqlconnection()
    db.row_factory=sqlite3.Row 
    cursor = db.cursor()
    statement = "SELECT * FROM usuarios WHERE id = ?;"
    cursor.execute(statement, [id])
    
    return cursor

# Funciona
def get_validarusuario(email):
    
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT id, nombre, email, estado FROM usuarios WHERE email = ?;"
    respuesta = cursor.execute(statement, [email]).fetchone()
   
    return respuesta

# Funciona
def get_login(email):
    try:
        #db = get_db()
        db = sqlconnection()
        db.row_factory=sqlite3.Row 
        cursor = db.cursor()
        statement = "SELECT * FROM usuarios WHERE email = ?"
        respuesta = cursor.execute(statement, [email]).fetchone()

        return respuesta

    except Error as err:
        print(err)
        
# Funciona  
def get_usuarios():
    db = sqlconnection()
    db.row_factory=sqlite3.Row 
    cur = db.cursor()
    cur.execute('SELECT * FROM usuarios;')
    row = cur.fetchall()
    return row


def delete_usuario(id):
    try:
        db = get_db()
        statement = "DELETE FROM usuarios WHERE id =?;"
        db.execute(statement,[id])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)