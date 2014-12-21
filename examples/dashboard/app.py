import sqlite3
import pandas as pd
# we add a new imports from flask
from flask import Flask, g, Response, render_template, request
# and we import the analysis tools
from analysis_tools import (get_data_from_db, date_resolution,
    metric_by_date, unique_users, minutes_watched,
    add_zeros_for_missing_dates, rank_titles)
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

def json_resp(df):
    return Response(df.to_json(), mimetype = 'application/json')

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/data/unique_users/")
def get_users():
    res = request.args.get("resolution")
    db = get_db()
    df = get_data_from_db(db)
    users = unique_users(df, res)
    users = add_zeros_for_missing_dates(users, res)
    return json_resp(users)

@app.route("/data/minutes_watched/")
def get_minutes_watched():
    res = request.args.get("resolution")
    db = get_db()
    df = get_data_from_db(db)
    mins = minutes_watched(df, res)
    mins = add_zeros_for_missing_dates(mins, res)
    return json_resp(mins)

@app.route("/data/toplist/")
def get_toplist():
    num = int(request.args.get("num"))
    db = get_db()
    df = get_data_from_db(db)
    top = rank_titles(df, num)
    return json_resp(top)

if __name__ == '__main__':
    app.run(port = 9009, debug = True)