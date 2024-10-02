from flask import Flask, request, redirect, render_template, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'
app.config["USERNAME"] = 'user'
app.config["PASSWORD"] = 'pass'

@app.route('/')
def index():
    if session.get("flag"):
        return render_template('welcome.html',username=session["username"])
    return redirect('/login')

@app.route('/login',methods=['GET'])
def login():
    if session.get("flag"):
        return redirect('/welcome')
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    if username != app.config['USERNAME']:
        flash('ユーザー名が異なります')
    elif password != app.config['PASSWORD']:
        flash('パスワードが異なります。')
    else:
        session['flag'] = True
        session["username"] = username
        return redirect('/welcome')
    
    return redirect('/login')

@app.route('/welcome')
def welcome():
    if session.get("flag"):
        return render_template('welcome.html',username=session["username"])
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
