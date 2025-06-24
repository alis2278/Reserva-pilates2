from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "🏋️‍♀️ Bot de reservas activo"

@app.route('/ping')
def ping():
    return "pong"
