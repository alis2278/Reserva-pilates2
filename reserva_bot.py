import os
from playwright.sync_api import sync_playwright
from utils import capturar_screenshot, enviar_correo

def ejecutar_reserva(email_gym, pass_gym):
    email_destino = os.getenv("EMAIL_DESTINO")
    email_remitente = os.getenv("EMAIL_REMITENTE")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://reservas.olympicgym.cl/accounts/login/?next=/")
            page.fill("#id_login", email_gym)
            page.fill("#id_password", pass_gym)
            page.click("button[type='submit']")
            page.wait_for_timeout(3000)

            if "Cerrar sesión" not in page.content():
                raise Exception(f"Login fallido para {email_gym}")

            page.goto("https://reservas.olympicgym.cl/classes/agenda/")
            page.wait_for_timeout(3000)

            reservado = False
            cards = page.query_selector_all(".class-card")

            for card in cards:
                texto = card.inner_text()
                if "Antonella" in texto and "08:15" in texto:
                    span = card.query_selector("span[id^='spn-agendar-text']")
                    if span and span.inner_text().strip() == "Reservar ahora":
                        span.click()
                        reservado = True
                        break

            mensaje = f"✅ [{email_gym}] Clase reservada con éxito" if reservado else f"⚠️ [{email_gym}] No se encontró clase para reservar"
            img = capturar_screenshot(page)
            enviar_correo(email_remitente, email_destino, mensaje, img)
            browser.close()

    except Exception as e:
        enviar_correo(email_remitente, email_destino, f"❌ [{email_gym}] Error: {str(e)}", None)
