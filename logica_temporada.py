from datetime import datetime, timezone
from whatsapp import enviar_whatsapp_canje, enviar_whatsapp_imagen
from generador_tarjetas import generar_tarjeta_temporada_base64

def procesar_promos_temporada(sesion, graphql_url):
    print("\n🍂 [TEMPORADA] Iniciando búsqueda de promociones estacionales vigentes...", flush=True)

    fecha_actual = datetime.now(timezone.utc).isoformat()

    # 1. Consultar temporadas activas vigentes hoy
    query_temporada = """
    query ObtenerTemporadasVigentes($fechaActual: DateTime!) {
      promocionTemporadas(
        where: {
          and: [
            { activo: { eq: true } }
            { fechaInicio: { lte: $fechaActual } }
            { fechaFin: { gte: $fechaActual } }
          ]
        }
      ) {
        nodes {
          nombre
        }
      }
    }
    """
    
    try:
        resp = sesion.post(graphql_url, json={
            "query": query_temporada,
            "variables": {"fechaActual": fecha_actual}
        })
        resp.raise_for_status()
        resultado = resp.json()
    except Exception as e:
        return {"status": "error", "message": f"Error al consultar temporadas: {e}"}, 500

    nodos_temporada = resultado.get("data", {}).get("promocionTemporadas", {}).get("nodes", [])
    
    if not nodos_temporada:
        print("❄️ No hay ninguna promoción de temporada activa el día de hoy.", flush=True)
        return {"status": "success", "message": "Sin temporadas vigentes hoy"}, 200

    print(f"🌟 Temporadas activas encontradas: {len(nodos_temporada)}. Se enviará una tarjeta por cada evento.", flush=True)

    # 2. Obtener TODOS los clientes
    query_clientes = """
    query ObtenerTodosLosClientes {
      clientes {
        nodes {
          id
          nombre
          celular
        }
      }
    }
    """
    try:
        resp_clientes = sesion.post(graphql_url, json={"query": query_clientes})
        resp_clientes.raise_for_status()
        nodos_clientes = resp_clientes.json().get("data", {}).get("clientes", {}).get("nodes", [])
    except Exception as e:
        return {"status": "error", "message": f"Error clientes: {e}"}, 500

    # 3. Procesar envíos (Una iteración separada por CADA temporada activa)
    mensajes_enviados = 0
    
    for temporada in nodos_temporada:
        nombre_temporada = temporada.get("nombre", "Especial")
        print(f"\n📋 Preparando envíos para el evento: *{nombre_temporada}*...", flush=True)

        for cliente in nodos_clientes:
            nombre_cliente = str(cliente.get("nombre", "")).strip()
            celular = cliente.get("celular")

            if nombre_cliente.lower() in ["anonimo", "anónimo", "cliente anonimo", "", "anonimo(sin registro)"] or not celular:
                continue

            # 🎨 Generamos el cupón visual INDIVIDUAL para esta temporada específica
            imagen_b64 = generar_tarjeta_temporada_base64(nombre_cliente, nombre_temporada)

            # ⚠️ TEXTO DE RESPALDO (Solo se envía si el generador de imágenes se cae)
            mensaje_respaldo = (
                f"¡Hola, {nombre_cliente}! ✨ Estamos celebrando la temporada de *{nombre_temporada}* en Cafetería Yana ☕.\n\n"
                f"Por ser parte de nuestra familia, queremos regalarte un *10% de descuento* en todas tus compras. 🎉\n\n"
                f"🏃‍♂️ ¡Aprovechá que es por tiempo limitado! Solo mostrale este mensaje al cajero. 🍂🌟"
            )
            
            # 🖼️ Enviar SOLO LA IMAGEN pasándole "" como caption
            if imagen_b64:
                if enviar_whatsapp_imagen(nombre_cliente, celular, "", imagen_b64):
                    mensajes_enviados += 1
            else:
                if enviar_whatsapp_canje(nombre_cliente, celular, mensaje_respaldo):
                    mensajes_enviados += 1

    return {"status": "success", "message": f"Procesamiento ejecutado: {mensajes_enviados} tarjetas enviadas"}, 200