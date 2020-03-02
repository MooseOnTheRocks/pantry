# pantry.py

from flask import Flask, render_template, g, request, jsonify, redirect, url_for
import database
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/<int:user_id>')
@app.route('/')
def index(user_id=1):
    return render_template("index.html.jinja", user_id=user_id)

@app.route('/list/<int:user_id>')
def listfoods(user_id):
    fooditems = []
    with get_db().executeSQL("SELECT * FROM `pantry`") as pantry:
        user_products = filter(lambda x: x[0] == user_id, pantry)
        user_products = map(lambda x: (x[1], x[2]), user_products)
        user_products = list(user_products)
        print("User products:", user_products)
        for prod_id, quantity in user_products:
            with get_db().executeSQL(f"SELECT * FROM `products` WHERE prod_id={prod_id};") as product:
                for _, prod_name, _ in product:
                    fooditems.append((prod_name, quantity))
    print(fooditems)
    return render_template("list.html.jinja", user_id=user_id, fooditems=fooditems)

@app.route('/add/<int:user_id>', methods=["POST", "GET"])
def add(user_id):
    if request.method == "GET":
        return render_template("add.html.jinja", user_id=user_id)
    elif request.method == "POST":
        with get_db().executeSQL(f"SELECT EXISTS (SELECT * FROM `products` where `name`='{request.form['name']}');") as exists:
            if list(exists)[0] == (0,):
                with get_db().executeSQL(f"INSERT INTO `products` (`name`) VALUES ('{request.form['name']}');") as res:
                    print("Response:", str(list(res)))
        return redirect(f"/add/{user_id}")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html.jinja')
    elif request.method == "POST":
        userFoodName = request.form.get('food_name', None)
        query = "SELECT name FROM products WHERE name LIKE " + "'%" + userFoodName + "%';"
        with get_db().executeSQL(query) as rows:
            result = list(rows)
        print(result)
        return render_template('search.html.jinja', result=result)

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