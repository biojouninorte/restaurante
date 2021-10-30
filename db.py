import sqlite3
from sqlite3 import Error
from flask import g

database = "restaurante.db"

def sqlconnection():
    conn = sqlite3.connect(database)
    return conn



def get_db():

    try:
        
        if 'db' not in g:
            db = sqlite3.connect('restaurante.db',timeout=10)
        return db

    except Error:
        print(Error)


def close_db():
    if 'db' is not None:
        g.db.close()
