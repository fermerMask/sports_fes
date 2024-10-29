from flask import Flask,request,redirect,render_template,flash,session,send_file,url_for
import random
import time
import qrcode
import io


app = Flask(__name__)

MAX_WINNERS = 20


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw',methods=['POST'])
def draw():
    time.sleep(2)
    is_winner = random.choice([True, False])

    if is_winner:
        return redirect(url_for('winner'))
    else:
        return redirect(url_for('loser'))

@app.route('/winner')
def winner():
    return render_template('winner.html')

@app.route('/loser')
def loser():
    return render_template('loser.html')

@app.route('/ticket1')
def ticket_image():
    return send_file('static/assets/ticket1.jpg',minetype='image/jpg')

@app.route('/qrcode')
def generate_qr():
    ticket_url = url_for('ticket_image',_external=True)
    qr_img = qrcode.make(ticket_url)
    img_io = io.BytesIO()
    qr_img.save(img_io,'PNG')
    img_io.seek(0)
    return send_file(img_io,mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
