from keep_alive import app
from reserva_bot import ejecutar_reserva
from flask import request
import os

# Endpoint para test manual por cuenta
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

# Lanza el servidor Flask (esto es lo que Render espera)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
