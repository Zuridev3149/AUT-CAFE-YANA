from datetime import datetime, timezone
from whatsapp import enviar_whatsapp_canje

def procesar_promos_temporada(sesion, graphql_url):
    print("\n🍂 [TEMPORADA] Iniciando búsqueda de promociones estacionales vigentes...", flush=True)

    # Obtenemos la fecha y hora actual en formato ISO 8601 (UTC) para GraphQL
    fecha_actual = datetime.now(timezone.utc).isoformat()

    # 1. Consultar temporadas activas vigentes hoy y sus productos anidados
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
          productosCanjeables {
            productoCanjeable {
              nombreProducto
              puntos
            }
          }
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

    # Extraer y aplanar los productos de todas las temporadas vigentes
    nombres_temporadas = []
    productos_temporada = []
    
    for temporada in nodos_temporada:
        nombres_temporadas.append(temporada.get("nombre"))
        for pc in temporada.get("productosCanjeables", []):
            prod = pc.get("productoCanjeable")
            if prod:
                productos_temporada.append({
                    "nombreProducto": prod.get("nombreProducto"),
                    "puntos": prod.get("puntos", 0)
                })

    if not productos_temporada:
        return {"status": "success", "message": "Temporada activa pero sin productos asignados"}, 200

    puntos_minimos = min(p["puntos"] for p in productos_temporada)
    print(f"🌟 Temporadas activas: {', '.join(nombres_temporadas)}. Puntos mínimos: {puntos_minimos}", flush=True)

    # 2. Obtener clientes calificados
    query_clientes = """
    query ObtenerClientesCalificados($puntosMin: Int!) {
      clientes(where: { puntos: { gte: $puntosMin } }) {
        nodes { id nombre celular puntos }
      }
    }
    """
    try:
        resp_clientes = sesion.post(graphql_url, json={"query": query_clientes, "variables": {"puntosMin": puntos_minimos}})
        resp_clientes.raise_for_status()
        nodos_clientes = resp_clientes.json().get("data", {}).get("clientes", {}).get("nodes", [])
    except Exception as e:
        return {"status": "error", "message": f"Error clientes: {e}"}, 500

    # 3. Procesar clientes y enviar mensajes
    print(f"\n📋 Procesando {len(nodos_clientes)} cliente(s) para el menú de temporada...", flush=True)
    
    for cliente in nodos_clientes:
        nombre_cliente = str(cliente.get("nombre", "")).strip()
        celular = cliente.get("celular")
        puntos_cliente = cliente.get("puntos", 0)

        if nombre_cliente.lower() in ["anonimo", "anónimo", "cliente anonimo", "", "anonimo(sin registro)"] or not celular:
            continue

        # Filtrar solo los productos de temporada para los que le alcanza el saldo
        premios_disponibles = [p["nombreProducto"] for p in productos_temporada if puntos_cliente >= p["puntos"]]
        if not premios_disponibles:
            continue

        nombres_temp_str = " y ".join(nombres_temporadas)
        lista_premios_texto = "\n🍁 - ".join(premios_disponibles)
        
        # Mensaje con urgencia (FOMO)
        mensaje_final = (
            f"¡Hola, {nombre_cliente}! ✨ Llegó el menú de *{nombres_temp_str}* a Cafetería Yana ☕.\n\n"
            f"Tenés *{puntos_cliente} puntos* acumulados. ¡Suficientes para probar nuestras especialidades de temporada GRATIS! 🎉\n\n"
            f"Ya podés canjear tus puntos por:\n"
            f"🍁 - {lista_premios_texto}\n\n"
            f"🏃‍♂️ ¡Apurate que estos productos son por tiempo limitado! Avisale al cajero en tu próxima visita. 🍂🌟"
        )
        enviar_whatsapp_canje(nombre_cliente, celular, mensaje_final)

    return {"status": "success", "message": "Procesamiento de temporada ejecutado correctamente"}, 200