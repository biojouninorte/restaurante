from flask import Flask
from sqlite3 import Error
from db import sqlconnection, get_db



def insert_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by):
    #db = sqlconnection()
    try:
        db = get_db()
        #cursor = db.cursor()
        statement = "INSERT INTO usuarios (nombre, apellido, email, telefono, direccion, password, created_by, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        db.execute(statement, (nombre, apellido, email, telefono, direccion, password, created_by, updated_by))
        #db.cursor()
        print("Usuario llego", db)
        db.commit()
        
        db.close()
        return True
    except Error as err:
        print(err)
    
    

def update_usuario(nombre, apellido, email, telefono, direccion, password, created_by, updated_by):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "UPDATE usuarios SET(nombre = ?, apellido = ? email = ?, telefono = ?, direccion = ?, password = ?, created_by = ?, update_by = ?) WHERE id = ?;"
    cursor.execute(statement, [nombre, apellido, email, telefono, direccion, password, created_by, updated_by])
    cursor.commit()
    cursor.close()
    return True


def get_usuario(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT id, nombre, email, estado FROM usuarios WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True

def get_validarusuario(email):
    
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT id, nombre, email, estado FROM usuarios WHERE email = ?;"
    respuesta = cursor.execute(statement, [email]).fetchone()
   
    #cursor.commit()
    
    return respuesta

def get_usuarios():
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT * FROM usuarios;"
    cursor.execute(statement)
    #cursor.close()
    return cursor

def delete_usuarios(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "DELETE FROM usuarios WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True