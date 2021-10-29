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
    
    
# No probada
def update_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "UPDATE usuarios SET(nombre = ?, apellido = ? email = ?, telefono = ?, direccion = ?, password = ?, created_by = ?, update_by = ?) WHERE id = ?;"
    cursor.execute(statement, [nombre, apellido, email, telefono, direccion, password, created_by, updated_by])
    cursor.commit()
    cursor.close()
    return True

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
    cursor = db.cursor()
    statement = "SELECT * FROM usuarios;"
    cursor.execute(statement)
    #cursor.close()
    return cursor

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