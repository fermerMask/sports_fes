from flask import Flask, request, redirect, render_template, flash, session, jsonify
import sqlite3
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

MAX_WINNERS = 20  # 最大当選者数

def count_winners():
    conn = get_db_connection()
    winners_count = conn.execute('SELECT COUNT(*) FROM users WHERE result = "当たり"').fetchone()[0]
    conn.close()
    return winners_count

@app.route('/')
def index():
    if session.get("flag"):
        return render_template('welcome.html', username=session["username"])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        try:
            conn.execute('INSERT INTO users (username, password, result) VALUES (?, ?, ?)', (username, password, ''))
            conn.commit()
            flash('登録が完了しました。ログインしてください。')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('そのユーザー名は既に使用されています。')
            return redirect('/register')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    if session.get("flag"):
        return redirect('/welcome')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user is None:
        flash('ユーザー名かパスワードが異なります')
        return redirect('/login')
    else:
        session['flag'] = True
        session["username"] = username
        return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if session.get("flag"):
        return render_template('index.html', username=session["username"])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('flag', None)
    flash('ログアウトしました')
    return redirect("/login")

# 抽選エンドポイント
@app.route('/enter', methods=['POST'])
def enter_lottery():
    if not session.get("flag"):
        return jsonify({"error": "ログインが必要です"}), 403

    username = session["username"]

    conn = get_db_connection()
    
    # 現在ログイン中のユーザーの抽選結果を確認
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user["result"] != '':
        return redirect('')
        return jsonify({"error": f"すでに抽選済みです: {user['result']}"})

    # 当選者数を確認
    current_winners = count_winners()

    if current_winners >= MAX_WINNERS:
        return jsonify({"error": "すでに当選者数が上限に達しました。"})

    # 抽選結果の判定（50%の確率で当たり）
    is_winner = random.choice([True, False])

    if is_winner:
        result = '当たり'
        message = 'おめでとうございます！あなたは当選しました！'
    else:
        result = 'ハズレ'
        message = '残念ながら、ハズレです。またチャレンジしてください。'

    # 結果をデータベースに保存
    conn.execute('UPDATE users SET result = ? WHERE username = ?', (result, username))
    conn.commit()
    conn.close()

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)
