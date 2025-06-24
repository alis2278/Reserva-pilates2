import os
import time
from reserva_bot import ejecutar_reserva
from keep_alive import keep_alive
from flask import Flask, request

# Inicia el servidor Flask para mantener el bot vivo
keep_alive()

# Diccionario para manejar múltiples cuentas
CUENTAS = [
    {
        "email": os.getenv("EMAIL_GYM"),
        "pass": os.getenv("PASS_GYM"),
        "remitente": os.getenv("EMAIL_REMITENTE"),
        "destino": os.getenv("EMAIL_DESTINO")
    },
    {
        "email": os.getenv("EMAIL_GYM2"),
        "pass": os.getenv("PASS_GYM2"),
        "remitente": os.getenv("EMAIL_REMITENTE2"),
        "destino": os.getenv("EMAIL_DESTINO2")
    },
    {
        "email": os.getenv("EMAIL_GYM3"),
        "pass": os.getenv("PASS_GYM3"),
        "remitente": os.getenv("EMAIL_REMITENTE3"),
        "destino": os.getenv("EMAIL_DESTINO3")
    }
]

# Crea app Flask (ya activa desde keep_alive)
app = Flask(__name__)

@app.route("/test-reserva")
def test_reserva():
    cuenta_index = int(request.args.get("cuenta", 1)) - 1
    if 0 <= cuenta_index < len(CUENTAS):
        datos = CUENTAS[cuenta_index]
        print(f"🔄 Ejecutando prueba para cuenta {cuenta_index + 1}...")
        ejecutar_reserva(datos["email"], datos["pass"], datos["remitente"], datos["destino"])
        return f"✅ Reserva ejecutada para cuenta {cuenta_index + 1} ({datos['email']})"
    else:
        return "❌ Cuenta no válida"

# Loop principal para correr solo martes, jueves y domingo a las 7:00
def iniciar_loop():
    print("⏳ Bot activo y esperando horarios programados...")
    while True:
        ahora = time.localtime()
        if ahora.tm_wday in [1, 3, 6] and ahora.tm_hour == 7 and ahora.tm_min == 0:
            print("🚀 Ejecutando reservas programadas...")
            for datos in CUENTAS:
                ejecutar_reserva(datos["email"], datos["pass"], datos["remitente"], datos["destino"])
            print("✅ Reservas completadas.")
            time.sleep(60)  # Espera 1 minuto para evitar repeticiones
        time.sleep(20)

if __name__ == "__main__":
    iniciar_loop()
