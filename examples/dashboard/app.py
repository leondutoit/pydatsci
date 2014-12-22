import sqlite3
import pandas as pd
from flask import Flask, g, Response, render_template, request
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

def json_resp(df, format = "ts"):
    if format == "ts":
        df = pd.DataFrame({
            'date': df.index,
            'values': df.values})
    else:
        df = pd.DataFrame({
            'title': df.index,
            'values': df.values})
    return Response(
        df.to_json(orient = 'records'),
        mimetype = 'application/json')

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/data/<ts_metric>/")
def get_metric(ts_metric):
    res = request.args.get("resolution")
    db = get_db()
    df = get_data_from_db(db)
    if ts_metric == "unique_users":
        df = unique_users(df, res)
    elif ts_metric == "minutes_watched":
        df = minutes_watched(df, res)
    df = add_zeros_for_missing_dates(df, res)
    return json_resp(df)

@app.route("/data/toplist/")
def get_toplist():
    num = int(request.args.get("num"))
    db = get_db()
    df = get_data_from_db(db)
    top = rank_titles(df, num)
    return json_resp(top, format = "rank")

if __name__ == '__main__':
    app.run(port = 9009, debug = True)