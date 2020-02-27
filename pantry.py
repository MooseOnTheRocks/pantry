# pantry.py

from flask import Flask, render_template, g, request, jsonify, redirect, url_for
import database
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/myfood/list')
def myfood_list():
    with get_db().select("fooditems", "name", "category") as rows:
        fooditems = list(rows)
    return render_template("myfood_list.html.jinja", fooditems=fooditems)

@app.route('/myfood/add', methods=["GET"])
def myfood_add():
    return render_template("myfood_add.html.jinja")

@app.route('/myfood/addfooditem', methods=["POST"])
def myfood_addfooditem():
    print(request.form["name"], request.form["category"], request.form["calories"])
    return redirect(url_for("myfood_add"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html.jinja"), 404

# Helper functions for database access and connection lifetime.
def get_db():
    if not hasattr(g, "db_connection"):
        g.db_connection = database.connect(**DB_CONFIG)
    return g.db_connection

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db_connection"):
        g.db_connection.close()