from flask import Flask
from db import sqlconnection


def insert_producto(nombre, precio, cantidad):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "INSERT INTO producto(nombre, precio, cantidad) VALUES(?, ?, ?);"
    cursor.execute(statement, [nombre, precio, cantidad])
    cursor.commit()
    cursor.close()
    return True


def update_producto(nombre, precio, cantidad):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "UPDATE producto SET (nombre = ?, precio = ?, cantidad = ?) WHERE id = ?;"
    cursor.execute(statement, [nombre, precio, cantidad])
    cursor.commit()
    cursor.close()
    return True

def get_producto(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT id, nombre, precio, cantidad FROM producto WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True

def get_productos(query):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT * FROM producto;"
    cursor.execute(statement, [query])
    
    cursor.close()
    return True

def delete_producto(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "DELETE FROM producto WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True