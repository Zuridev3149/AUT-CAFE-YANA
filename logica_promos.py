from whatsapp import enviar_whatsapp_canje

def procesar_canjes_promocionales(sesion, graphql_url):
    print("\n📥 [PROMOS] Iniciando procesamiento de promos permanentes gratis...", flush=True)

    # 1. Obtener productos
    query_productos = """
    query ObtenerProductos { productosCanjeables { nodes { nombreProducto puntos } } }
    """
    try:
        resp = sesion.post(graphql_url, json={"query": query_productos})
        resp.raise_for_status()
        nodos_productos = resp.json().get("data", {}).get("productosCanjeables", {}).get("nodes", [])
    except Exception as e:
        return {"status": "error", "message": f"Error productos: {e}"}, 500

    if not nodos_productos:
        return {"status": "error", "message": "Sin productos canjeables en Azure"}, 500

    puntos_minimos = min(p.get("puntos", 0) for p in nodos_productos)

    # 2. Obtener Promos de ProductoGratis
    query_promos = """
    query ObtenerPromosProductoGratis {
      promocionPermanentes(where: { and: [{ activo: { eq: true } }, { tipoRecompensa: { eq: "ProductoGratis" } }] }) {
        nodes { nombre descripcion }
      }
    }
    """
    try:
        resp = sesion.post(graphql_url, json={"query": query_promos})
        nodos_promos = resp.json().get("data", {}).get("promocionPermanentes", {}).get("nodes", [])
    except Exception:
        nodos_promos = []

    # 3. Obtener clientes
    query_clientes = """
    query ObtenerClientesCalificados($puntosMin: Int!) {
      clientes(where: { puntos: { gte: $puntosMin } }) {
        nodes { id nombre celular puntos }
      }
    }
    """
    try:
        resp = sesion.post(graphql_url, json={"query": query_clientes, "variables": {"puntosMin": puntos_minimos}})
        resp.raise_for_status()
        nodos_clientes = resp.json().get("data", {}).get("clientes", {}).get("nodes", [])
    except Exception as e:
        return {"status": "error", "message": f"Error clientes: {e}"}, 500

    if not nodos_clientes:
        print("📉 Ningún cliente califica para canje en este momento.", flush=True)
        return {"status": "success", "message": "Sin clientes calificados para canje"}, 200

    # 4. Procesamiento y envío
    print(f"\n📋 Procesando {len(nodos_clientes)} cliente(s) calificado(s)...", flush=True)
    for cliente in nodos_clientes:
        nombre_cliente = str(cliente.get("nombre", "")).strip()
        celular = cliente.get("celular")
        puntos_cliente = cliente.get("puntos", 0)

        if nombre_cliente.lower() in ["anonimo", "anónimo", "cliente anonimo", "cliente anónimo", "", "anonimo(sin registro)"] or not celular:
            continue

        premios_disponibles = [p.get("nombreProducto") for p in nodos_productos if puntos_cliente >= p.get("puntos", 0)]
        if not premios_disponibles:
            continue

        texto_promociones = ""
        if nodos_promos:
            texto_promociones = "\n\n🎁 *¡Aprovechá también nuestros productos GRATIS vigentes!* 🌟"
            for promo in nodos_promos:
                texto_promociones += f"\n✨ *{promo.get('nombre')}*: {promo.get('descripcion')}"

        lista_premios_texto = "\n☕ - ".join(premios_disponibles)
        mensaje_final = (
            f"¡Hola, {nombre_cliente}! ✨ Qué gusto saludarte desde *Cafetería Yana* ☕.\n\n"
            f"Queremos contarte que tenés un saldo de *{puntos_cliente} puntos* acumulados en tu cuenta. 🙌🎉\n\n"
            f"¡Con esos puntos *ya podés canjear GRATIS* cualquiera de estos productos en tu próxima visita:\n"
            f"☕ - {lista_premios_texto}"
            f"{texto_promociones}\n\n"
            f"🎁 Solo avisale al cajero en tu siguiente compra y ¡date un gustito por cuenta de la casa! ¡Te esperamos! 🧁🌟"
        )
        enviar_whatsapp_canje(nombre_cliente, celular, mensaje_final)

    return {"status": "success", "message": "Procesamiento masivo ejecutado correctamente"}, 200