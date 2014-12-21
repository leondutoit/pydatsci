
import sqlite3
import pandas as pd
from flask import Flask, g, Response
app = Flask(__name__)

DATABASE = 'moviedb'

def connect_to_database():
    conn = sqlite3.connect(DATABASE)
    return conn

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello():
    db = get_db()
    res = pd.read_sql('select * from movies limit 10', db)
    return Response(res.to_json(), mimetype = 'application/json')

if __name__ == '__main__':
    app.run(port = 9009, debug = True)
