from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import uuid
import random

app = Flask(__name__)

DATABASE = 'lottery.db'
MAX_WINNERS = 20

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    
    db.commit()
    db.close()

@app.before_request
def setup_database():
    if not os.path.exists(DATABASE):
        init_db()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter',methods=['POST'])
def enter_lottery():
    data = request.json
    name = data.get('name')

    print('受け取ったデータ:', data)

    user_id = str(uuid.uuid4())
    db = get_db()

    cursor = db.cursor()

    try:
        cursor.execute('BEGIN TRANSACTION')
        cursor.execute('SELECT COUNT(*) FROM winners')
        winner_count = cursor.fetchone()[0]

        if winner_count >= MAX_WINNERS:
            db.rollback()
            return jsonify({'message': 'All winners have already been selected'}),400
        
        if random.random() > 0.5:
            cursor.execute(('INSERT INTO winners (user_id, name) VALUES (?,?)'), (user_id,name))
            db.commit()
            return jsonify({'message': 'You have won!', 'user_id':user_id}),200
        else:
            db.commit()
            return jsonify({'message': 'Sorry, you did not win this time.'}),200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error':str(e)}),500
    
    finally:
        db.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

