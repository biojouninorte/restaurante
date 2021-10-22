import sqlite3
from flask import Flask
from db import sqlconnection


def insert_bebida(nombre, precio, cantidad):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "INSERT INTO bebidas(nombre, precio, cantidad) VALUES(?, ?, ?);"
    cursor.execute(statement, [nombre, precio, cantidad])
    cursor.commit()
    cursor.close()
    return True


def update_bebida(nombre, precio, cantidad):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "UPDATE bebidas SET (nombre = ?, precio = ?, cantidad = ?) WHERE id = ?;"
    cursor.execute(statement, [nombre, precio, cantidad])
    cursor.commit()
    cursor.close()
    return True

def get_bebida(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT id, nombre, precio, cantidad FROM bebidas WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True

def get_bebidas(query):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "SELECT * FROM bebidas;"
    cursor.execute(statement, [query])
    
    cursor.close()
    return True

def list_bebidas():
    db = sqlconnection()
    db.row_factory=sqlite3.Row # Convierte la respuesta de la BD en un diccionario
    cur = db.cursor()  #manipular la conxion de la BD
    cur.execute('SELECT * FROM bebidas;')
    row = cur.fetchall()
    return row

def delete_bebidas(id):
    db = sqlconnection()
    cursor = db.cursor()
    statement = "DELETE FROM bebidas WHERE id = ?;"
    cursor.execute(statement, [id])
    cursor.commit()
    cursor.close()
    return True