# Ir al panel principal tras login
page.goto("https://reservas.olympicgym.cl", timeout=60000)
page.wait_for_timeout(2000)

# Hacer clic en el botón de menú 'Agenda'
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

if not encontrada:
    print("❌ No se encontró clase con Antonella a las 08:15.")
