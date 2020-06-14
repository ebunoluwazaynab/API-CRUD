from flask import Flask, request, jsonify
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "apiDb.db")
app = Flask(__name__)


@app.route('/item', methods=['GET'])
def api_get_all():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        query = 'SELECT * FROM items'
        wds = cur.execute(query).fetchall()
        return jsonify(wds)

@app.route('/item/<int:id>', methods=['GET'])
def api_get_id(id):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        query = 'SELECT * FROM items WHERE id = ?', id
        product = cur.execute(query).fetchall()
        return jsonify(product)

@app.route('/item', methods=['POST'])
def api_post():
    id = request.args['id']
    name = request.args['name']
    price = request.args['price']
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        item = (id, name, price)
        cur.execute('INSERT INTO items(id,Name,Price) VALUES (?,?,?)', item)
        conn.commit()
    return jsonify('Posted'), 200
    conn.close()


@app.route('/item', methods=['DELETE'])
def api_delete():
    id = request.args['id']
    with sqlite3.connect(db_path) as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM items WHERE id = ?', id)
            return jsonify('SUCCESS'), 200
        except:
            "No Record Found for Deletion"


@app.route('/item', methods=['PUT'])
def api_update():
    with sqlite3.connect(db_path) as conn:
        id = request.args['id']
        name = request.args['name']
        price = request.args['price']
        cur = conn.cursor()
        #query = 'UPDATE products SE'
        cur.execute('UPDATE items SET price = ?, name = ? WHERE id = ?', (price, name, id))
        conn.commit()
        return jsonify('Updated'), 200


app.run(debug=True)
