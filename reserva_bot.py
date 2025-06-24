from playwright.sync_api import sync_playwright
from utils import capturar_screenshot, enviar_correo
import os
import traceback

URL_LOGIN = "https://reservas.olympicgym.cl/accounts/login/?next=/"

def ejecutar_reserva(email_gym, pass_gym):
    if not email_gym or not pass_gym:
        print(f"⚠️ Credenciales faltantes. Se omite cuenta.")
        return

    print(f"🔐 Iniciando reserva para {email_gym}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            context = browser.new_context()
            page = context.new_page()

            # Login
            page.goto(URL_LOGIN, timeout=60000)
            page.fill('input[name="username"]', email_gym)
            page.fill('input[name="password"]', pass_gym)
            page.click('button[type="submit"]')
            page.wait_for_timeout(3000)

            if "Cerrar sesión" not in page.content():
                raise Exception("⚠️ Login fallido")

            # Ir al panel principal
            page.goto("https://reservas.olympicgym.cl", timeout=60000)
            page.wait_for_timeout(2000)

            # Hacer clic en "Agenda"
            try:
                page.wait_for_selector("text=Agenda", timeout=10000)
                page.click("text=Agenda")
                print("📋 Se accedió correctamente a la sección Agenda.")
                page.wait_for_timeout(3000)
            except:
                raise Exception("❌ No se pudo hacer clic en 'Agenda'")

            # Buscar clases
            clases = page.locator("div.class-info")
            encontrada = False

            for i in range(clases.count()):
                clase = clases.nth(i)
                texto = clase.inner_text()

                if "Antonella" in texto and "08:15" in texto:
                    if "Reservar ahora" in texto:
                        print("✅ Clase encontrada. Reservando...")
                        clase.click()
                        encontrada = True
                        break
                    else:
                        print("⏳ Clase aún no disponible para reservar.")
                        encontrada = True
                        break

            nombre_img = capturar_screenshot(page, f"{email_gym}_ok.png")

            if not encontrada:
                print("❌ No se encontró clase con Antonella a las 08:15.")

            enviar_correo(
                os.getenv("EMAIL_REMITENTE"),
                os.getenv("EMAIL_DESTINO"),
                f"🔔 [{email_gym}] Resultado reserva",
                nombre_img
            )

            browser.close()

    except Exception as e:
        print(f"❌ Error para {email_gym}: {e}")
        traceback.print_exc()
        nombre_img = "error.png"
        enviar_correo(
            os.getenv("EMAIL_REMITENTE"),
            os.getenv("EMAIL_DESTINO"),
            f"❌ [{email_gym}] Error: {str(e)}",
            capturar_screenshot(page, nombre_img) if 'page' in locals() else None
        )
