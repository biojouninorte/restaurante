import sqlite3
from flask import Flask
from sqlite3 import Error
from db import sqlconnection, get_db, close_db


def agregar_favoritos(bebida_id):
    try:
        db = get_db()
        statement = "INSERT INTO listaDeseos(id, bebida_id) VALUES(?, ?);"
        db.execute(statement, [id, bebida_id])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)

def get_favoritos():
    db = sqlconnection()
    db.row_factory=sqlite3.Row 
    cur = db.cursor()  
    cur.execute('SELECT * FROM listaDeseos;')
    row = cur.fetchall()
    return row

def delete_favorito(id):
    try:
        db = get_db()
        statement = "DELETE FROM listaDeseos WHERE id =?;"
        db.execute(statement,[id])
        db.commit()
        db.close()
        return True
    except Error as err:
        print(err)