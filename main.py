import os
import time
from reserva_bot import ejecutar_reserva
from keep_alive import keep_alive
from flask import Flask, request

# Mantener servicio vivo
keep_alive()

# Flask para prueba manual desde navegador
app = Flask(__name__)

@app.route("/")
def home():
    return "🏋️‍♀️ Bot de reservas activo"

@app.route("/ping")
def ping():
    return "pong"

@app.route("/test-reserva")
def test_reserva():
    cuenta = request.args.get("cuenta", "1")
    email = os.getenv(f"EMAIL_GYM{cuenta if cuenta != '1' else ''}")
    password = os.getenv(f"PASS_GYM{cuenta if cuenta != '1' else ''}")
    if email and password:
        try:
            ejecutar_reserva(email, password)
            return f"✅ Reserva ejecutada para cuenta {cuenta} ({email})"
        except Exception as e:
            return f"❌ Error ejecutando reserva: {str(e)}"
    else:
        return "⚠️ Credenciales no encontradas."

# Loop automático (opcional, ya lo tienes si querés usarlo también)
def iniciar_loop():
    print("⏳ Bot activo y esperando horarios programados...")
    while True:
        ahora = time.localtime()
        if ahora.tm_hour == 7 and ahora.tm_wday in [1, 3, 6]:  # Martes=1, Jueves=3, Domingo=6
            print("🕖 Ejecutando reservas programadas...")
            for i in range(1, 4):
                email = os.getenv(f"EMAIL_GYM{i if i > 1 else ''}")
                password = os.getenv(f"PASS_GYM{i if i > 1 else ''}")
                ejecutar_reserva(email, password)
            time.sleep(60 * 60)  # Espera 1 hora para evitar duplicados
        time.sleep(20)

# Activar el loop (descomentá si querés que funcione además del modo test)
# iniciar_loop()
