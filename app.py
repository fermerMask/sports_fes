from flask import Flask, request, redirect, render_template, flash, session, jsonify
from supabase import create_client, Client
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

# SupabaseのURLとキーを設定

# Supabaseクライアントを初期化
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

MAX_WINNERS = 20  # 最大当選者数

def count_winners():
    # Supabaseから当選者数を取得
    response = supabase.table('users').select('result').eq('result', '当たり').execute()
    winners_count = len(response.data)
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

        try:
            # Supabaseに新しいユーザーを登録
            supabase.table('users').insert({'username': username, 'password': password, 'result': ''}).execute()
            flash('登録が完了しました。ログインしてください。')
            return redirect('/login')
        except Exception as e:
            flash('そのユーザー名は既に使用されています。')
            return redirect('/register')
    
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

    # Supabaseからユーザー情報を取得
    response = supabase.table('users').select('*').eq('username', username).eq('password', password).execute()

    if len(response.data) == 0:
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

    # Supabaseから現在ログイン中のユーザーの抽選結果を取得
    response = supabase.table('user').select('*').eq('username', username).execute()
    user = response.data[0]

    if user["result"] != '':
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

    # 結果をSupabaseに保存
    supabase.table('users').update({'result': result}).eq('username', username).execute()

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)
