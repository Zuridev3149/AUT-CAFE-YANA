import requests

EVOLUTION_URL = "http://evolution_api:8080/message/sendText/Yana_Bot"
EVOLUTION_APIKEY = "yana_secret_key"

def enviar_whatsapp_canje(nombre, celular, mensaje):
    """Envía el mensaje por WhatsApp a través de Evolution API"""
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