import sqlite3
from flask import Flask
from sqlite3 import Error
from db import sqlconnection, get_db, close_db


def agregar_favoritos(bebida_id, usuario_id):
    try:
        db = get_db()
        statement = "INSERT INTO favoritos(bebida_id, usuario_id) VALUES(?, ?);"
        db.execute(statement, [bebida_id, usuario_id])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)

def get_favoritos(usuario_id):
    db = sqlconnection()
    db.row_factory=sqlite3.Row 
    cur = db.cursor()  
    statement = ('SELECT * FROM favoritos WHERE usuario_id = ?;')
    cur.execute(statement,[usuario_id])
    row = cur.fetchall()
    return row

def delete_favorito(id):
    try:
        db = get_db()
        statement = "DELETE FROM favoritos WHERE id =?;"
        db.execute(statement,[id])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)