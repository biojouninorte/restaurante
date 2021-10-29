import sqlite3
from flask import Flask
from sqlite3 import Error
from db import sqlconnection, get_db, close_db

# Funciona
def insert_pedido(usuario_id, bebida_id, valor, direccion, created_by, updated_by):
    try:
        db = get_db()
        statement = "INSERT INTO pedidos(usuario_id, bebida_id, valor, direccion, created_by, updated_by) VALUES(?, ?, ?, ?, ?, ?);"
        db.execute(statement, [usuario_id, bebida_id, valor, direccion, created_by, updated_by])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)

# Funciona
def get_pedidos():
    db = sqlconnection()
    db.row_factory=sqlite3.Row # Convierte la respuesta de la BD en un diccionario
    cur = db.cursor()  #manipular la conxion de la BD
    cur.execute('SELECT * FROM pedidos;')
    row = cur.fetchall()
    return row

