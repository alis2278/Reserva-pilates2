from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "🏋️‍♀️ Bot de reservas activo"

@app.route('/ping')
def ping():
    return "pong"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
