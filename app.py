from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 初期設定: あたりの人数は20人
remaining_prizes = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
    global remaining_prizes
    if remaining_prizes > 0:
        # ランダムで「当たり」か「はずれ」を決めるが、当たりの人数が残っていれば当たりが出る
        result = random.choice(['当たり', 'はずれ']) if remaining_prizes > 0 else 'はずれ'
        if result == '当たり':
            remaining_prizes -= 1  # 当たりが出たら人数を減らす
    else:
        result = 'はずれ'  # あたり人数が0の場合は必ずはずれ
    return jsonify(result=result, remaining=remaining_prizes)

if __name__ == '__main__':
    app.run(debug=True)
