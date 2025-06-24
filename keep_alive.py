from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "🏋️‍♀️ Bot de reservas activo"

@app.route('/ping')
def ping():
    return "pong"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
