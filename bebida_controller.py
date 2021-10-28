import sqlite3
from flask import Flask
from sqlite3 import Error
from db import sqlconnection, get_db, close_db

# Funciona
def insert_bebida(nombreBebida, descripcion, precio, estado, created_by, updated_by):
    try:
        db = get_db()
        statement = "INSERT INTO bebidas(nombreBebida, descripcion, precio, estado, created_by, updated_by) VALUES(?, ?, ?, ?, ?, ?);"
        db.execute(statement, [nombreBebida, descripcion, precio, estado, created_by, updated_by])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)

# No probada
def update_bebida(nombre, precio, cantidad):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "UPDATE bebidas SET (nombre = ?, precio = ?, cantidad = ?) WHERE id = ?;"
    cursor.execute(statement, [nombre, precio, cantidad])
    cursor.commit()
    cursor.close()
    return True

# No probada
def get_bebida(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT id, nombre, precio, cantidad FROM bebidas WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True


# Funciona
def get_bebidas():
    db = sqlconnection()
    db.row_factory=sqlite3.Row # Convierte la respuesta de la BD en un diccionario
    cur = db.cursor()  #manipular la conxion de la BD
    cur.execute('SELECT * FROM bebidas;')
    row = cur.fetchall()
    return row

# No probada
def delete_bebidas(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "DELETE FROM bebidas WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True