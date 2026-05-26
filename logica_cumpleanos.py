from datetime import datetime

# 💡 IMPORTANTE: Traemos ambas funciones y el generador
from whatsapp import enviar_whatsapp_imagen, enviar_whatsapp_canje
from generador_tarjetas import generar_tarjeta_base64

def procesar_cumpleanos(sesion, graphql_url):
    print("\n🎂 [CUMPLEAÑOS] Iniciando búsqueda de cumpleañeros del día...", flush=True)

    query = """
    {
      clientes {
        nodes {
          nombre
          fecha_nacimiento
          estado
          celular
          correo
        }
      }
    }
    """

    # 1. Consultar a Azure
    try:
        response = sesion.post(graphql_url, json={"query": query})
        response.raise_for_status()
        clientes_data = response.json()
    except Exception as e:
        return {"status": "error", "message": f"Error al consultar GraphQL: {e}"}, 500

    lista_clientes = clientes_data.get("data", {}).get("clientes", {}).get("nodes", [])
    
    if not lista_clientes:
        return {"status": "error", "message": "No se encontraron clientes o el JSON es inválido"}, 500

    # 2. Filtrar cumpleañeros de hoy
    hoy = datetime.now()
    dia_mes_hoy = f"{hoy.day}/{hoy.month}"
    encontrados = []

    for cliente in lista_clientes:
        nombre = cliente.get("nombre", "Cliente")
        fecha_nac = cliente.get("fecha_nacimiento")
        estado = cliente.get("estado")
        celular = cliente.get("celular")

        if str(estado).lower() not in ["true", "activo", "1"]:
            continue
        if not fecha_nac or not celular:
            continue

        try:
            if "/" in fecha_nac:
                partes = fecha_nac.split("/")
                dia_mes_cliente = f"{int(partes[0])}/{int(partes[1])}"
            elif "-" in fecha_nac:
                fecha_limpia = fecha_nac.split("T")[0]
                dt = datetime.strptime(fecha_limpia, "%Y-%m-%d")
                dia_mes_cliente = f"{dt.day}/{dt.month}"
            else:
                continue
        except Exception:
            continue

        if dia_mes_cliente == str(dia_mes_hoy):
            encontrados.append(cliente)

    print(f"🚀 ¡Se encontraron {len(encontrados)} cumpleañeros listos!\n", flush=True)

    # 3. Enviar mensajes
    if len(encontrados) > 0:
        print("🚀 INICIANDO CAMPAÑA DE MENSAJES DE CUMPLEAÑOS...", flush=True)
        for cumpleanero in encontrados:
            nombre = cumpleanero.get('nombre')
            celular = cumpleanero.get('celular')
            
            # 🎨 Generamos la tarjeta visual en Base64
            imagen_b64 = generar_tarjeta_base64(nombre)
            
            if imagen_b64:
                # 🖼️ Pasamos un string vacío ("") en el campo de texto para que mande SÓLO la imagen
                enviar_whatsapp_imagen(nombre, celular, "", imagen_b64)
            else:
                # ⚠️ FALLBACK: Si imgkit falla por alguna razón, mandamos un texto simple como respaldo
                mensaje_auxiliar = f"¡Feliz Cumpleaños {nombre}! 🥳🎁 Pasa por Cafetería Yana hoy para reclamar tu regalito sorpresa."
                enviar_whatsapp_canje(nombre, celular, mensaje_auxiliar)
    else:
        print("☕ No hay cumpleañeros hoy.", flush=True)

    return {"status": "success", "message": f"Campaña finalizada. {len(encontrados)} mensajes enviados."}, 200