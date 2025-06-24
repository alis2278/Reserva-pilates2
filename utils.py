import os
import base64
from mailjet_rest import Client
from datetime import datetime

def capturar_screenshot(page):
    nombre = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = f"/tmp/{nombre}"
    try:
        page.screenshot(path=path)
        print(f"📸 Captura guardada en: {path}")
        return path
    except Exception as e:
        print(f"❌ Error capturando imagen: {e}")
        return None

def enviar_correo(remitente, destino, asunto, imagen_path):
    if not imagen_path or not os.path.exists(imagen_path):
        print(f"📭 No se adjuntó imagen (no existe o no se pudo capturar).")
        imagen_base64 = None
    else:
        try:
            with open(imagen_path, "rb") as img_file:
                imagen_base64 = base64.b64encode(img_file.read()).decode()
        except Exception as e:
            print(f"❌ Error leyendo la imagen: {e}")
            imagen_base64 = None

    mailjet = Client(auth=(
        os.getenv("MJ_APIKEY_PUBLIC"),
        os.getenv("MJ_APIKEY_PRIVATE")
    ), version='v3.1')

    mensaje = {
        'From': {"Email": remitente, "Name": "Bot Reservas"},
        'To': [{"Email": destino}],
        'Subject': asunto,
        'TextPart': "Resultado del intento de reserva."
    }

    if imagen_base64:
        mensaje["Attachments"] = [{
            "ContentType": "image/png",
            "Filename": "captura.png",
            "Base64Content": imagen_base64
        }]

    data = { 'Messages': [mensaje] }

    result = mailjet.send.create(data=data)
    print("📬 Correo enviado:", result.status_code)
    print("📦 Respuesta Mailjet:", result.json())
