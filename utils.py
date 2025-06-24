import os
import base64
from mailjet_rest import Client
from datetime import datetime

def capturar_screenshot(page):
    nombre = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = f"/tmp/{nombre}"
    page.screenshot(path=path)
    return path

def enviar_correo(remitente, destino, asunto, imagen_path):
    mailjet = Client(auth=(os.getenv("MJ_APIKEY_PUBLIC"), os.getenv("MJ_APIKEY_PRIVATE")), version='v3.1')

    attachments = []
    if imagen_path and os.path.exists(imagen_path):
        with open(imagen_path, "rb") as img_file:
            base64_img = base64.b64encode(img_file.read()).decode()
        attachments = [{
            "ContentType": "image/png",
            "Filename": "captura.png",
            "Base64Content": base64_img
        }]

    data = {
        'Messages': [{
            "From": {"Email": remitente, "Name": "Bot Reservas"},
            "To": [{"Email": destino}],
            "Subject": asunto,
            "TextPart": "Resultado del intento de reserva.",
            "Attachments": attachments
        }]
    }
    mailjet.send.create(data=data)
