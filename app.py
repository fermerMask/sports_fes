from flask import Flask, request, redirect, render_template, flash, session
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if session.get("flag"):
        return render_template('welcome.html',username=session["username"])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('登録が完了しました。ログインしてください。')
            return redirect('/login')  # 登録成功後にログインページにリダイレクト
        except sqlite3.IntegrityError:
            flash('そのユーザー名は既に使用されています。')
            return redirect('/register')  # エラー時は再度登録ページを表示
        finally:
            conn.close()
    
    # GETリクエストの場合は登録フォームを表示
    return render_template('register.html')  # 登録フォームを返す

            
@app.route('/login',methods=['GET'])
def login():
    if session.get("flag"):
        return redirect('/login')
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',(username,password)).fetchone()
    conn.close()

    if user is None:
        flash('ユーザー名が異なります')
        return redirect('/login')
    else:
        session['flag'] = True
        session["username"] = username
        return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if session.get("flag"):
        return render_template('index.html',username=session["username"])
    return redirect('/login')

@app.route('/content')
def contents():
    if session.get("flag"):
        return render_template('contents.html',username=session["username"])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('flag',None)
    session["username"] = None
    session['flag'] = False
    flash('ログアウトしました')
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)
