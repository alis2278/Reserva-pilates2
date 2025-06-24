from keep_alive import keep_alive, app
from reserva_bot import ejecutar_reserva
from flask import request
import os

# Inicia servidor Flask para mantener el bot activo (ping con UptimeRobot)
keep_alive()

# Endpoint para monitoreo
@app.route("/")
def home():
    return "🏋️‍♀️ Bot de reservas activo"

@app.route("/ping")
def ping():
    return "pong"

# Endpoint de prueba manual por cuenta
@app.route("/test-reserva")
def test_reserva():
    cuenta = request.args.get("cuenta", "1")
    email = os.getenv(f"EMAIL_GYM{cuenta}") or os.getenv("EMAIL_GYM")
    password = os.getenv(f"PASS_GYM{cuenta}") or os.getenv("PASS_GYM")

    try:
        ejecutar_reserva(email, password)
        return f"✅ Reserva ejecutada para cuenta {cuenta} ({email})"
    except Exception as e:
        return f"❌ Error ejecutando reserva: {e}"

# Si más adelante quieres activar un loop, este sería el lugar:
# import time
# def iniciar_loop():
#     while True:
#         ahora = datetime.now()
#         if ahora.weekday() in [1, 3, 6] and ahora.strftime("%H:%M") == "07:00":
#             ejecutar_reserva(...)
#         time.sleep(60)
# iniciar_loop()
