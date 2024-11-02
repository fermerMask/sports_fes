from flask import Flask, request, redirect, render_template, flash, session, send_file, url_for
import random
import time
import qrcode
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理のための秘密キー

MAX_WINNERS = 20  # 各部の当選上限人数


PARTS = ["1部", "2部", "3部", "4部"]

TICKET_IMAGES = {
    "1部": "ticket1.jpg",
    "2部": "ticket2.jpg",
    "3部": "ticket3.jpg",
    "4部": "ticket4.jpg"
}

@app.route('/')
def index():

    return render_template('index.html', parts=PARTS)

@app.route('/choose', methods=['POST'])
def choose():
    selected_part = request.form.get("selected_part")
    if selected_part not in PARTS:
        flash("無効な選択です。")
        return redirect(url_for('index'))
    
    session['selected_part'] = selected_part

    if 'win_counts' not in session:
        session['win_counts'] = {part: 0 for part in PARTS}
    
    return redirect(url_for('entry'))

@app.route('/entry')
def entry():

    return render_template('entry.html')

@app.route('/draw', methods=['POST'])
def draw():
    time.sleep(2) 
    
    selected_part = session.get('selected_part')
    if not selected_part:
        return redirect(url_for('index'))
    
    win_counts = session['win_counts']

    if win_counts[selected_part] >= MAX_WINNERS:
        return redirect(url_for('lose'))

    is_winner = random.choice([True, False])

    if is_winner:
        
        win_counts[selected_part] += 1
        session['win_counts'] = win_counts 
        return redirect(url_for('winner', ticket_image=TICKET_IMAGES[selected_part]))
    else:
        return redirect(url_for('lose'))

@app.route('/winner')
def winner():

    ticket_image = request.args.get('ticket_image')
    return render_template('winner.html', ticket_image=ticket_image)

@app.route('/lose')
def lose():
    
    return render_template('loser.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
