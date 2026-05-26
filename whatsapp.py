import requests

# URLs separadas para texto e imágenes
EVOLUTION_URL = "http://evolution_api:8080/message/sendText/Yana_Bot"
EVOLUTION_MEDIA_URL = "http://evolution_api:8080/message/sendMedia/Yana_Bot"
EVOLUTION_APIKEY = "yana_secret_key"

def enviar_whatsapp_canje(nombre, celular, mensaje):
    """Envía el mensaje de texto por WhatsApp a través de Evolution API"""
    print(f"   📲 Enviando WhatsApp a {nombre}...", flush=True)

    numero_limpio = str(celular).strip()
    if not numero_limpio.startswith("591"):
        numero_limpio = f"591{numero_limpio}"

    payload = {"number": numero_limpio, "text": mensaje}
    headers = {"apikey": EVOLUTION_APIKEY, "Content-Type": "application/json"}

    try:
        requests.post(EVOLUTION_URL, json=payload, headers=headers).raise_for_status()
        print(f"   ✅ Mensaje enviado a {nombre} ({numero_limpio})", flush=True)
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error al enviar WhatsApp a {nombre}: {e}", flush=True)
        return False

def enviar_whatsapp_imagen(nombre, celular, mensaje_texto, imagen_base64):
    """Envía una imagen Base64 con un texto descriptivo por Evolution API"""
    print(f"   📲 Enviando Tarjeta de Cumpleaños a {nombre}...", flush=True)

    numero_limpio = str(celular).strip()
    if not numero_limpio.startswith("591"):
        numero_limpio = f"591{numero_limpio}"

    # El payload exacto para enviar archivos multimedia (imágenes) en Evolution API
    # payload = {
    #     "number": numero_limpio,
    #     "mediatype": "image",
    #     "mimetype": "image/jpeg",
    #     "caption": mensaje_texto,
    #     "media": imagen_base64
    # }
# El payload exacto para enviar archivos multimedia en Evolution API
    payload = {
        "number": numero_limpio,
        "mediatype": "image",
        "mimetype": "image/png",  # <--- CAMBIA ESTO DE jpeg A png
        "caption": mensaje_texto,
        "media": imagen_base64
    }
    headers = {"apikey": EVOLUTION_APIKEY, "Content-Type": "application/json"}

    try:
        requests.post(EVOLUTION_MEDIA_URL, json=payload, headers=headers).raise_for_status()
        print(f"   ✅ ¡Tarjeta enviada con éxito a {nombre} ({numero_limpio})!", flush=True)
        return True
    except Exception as e:
        print(f"   ❌ Error al enviar imagen a {nombre}: {e}", flush=True)
        return False