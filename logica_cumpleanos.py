from datetime import datetime
# Reutilizamos la función de envío de tu módulo whatsapp
from whatsapp import enviar_whatsapp_canje

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
            
            mensaje = (
                f"¡Buen día, {nombre}! ¡Qué alegría saludarte en este día tan especial! 🥳\n\n"
                f"Desde aquí, de tu *Cafetería Yana*, te mandamos un abrazo bien 'rompe costillas', "
                f"cargado de todo el cariño cochabambino. ¡Que pases un cumple de maravilla, rodeado de tu gente y con mucha salud, pues!\n\n"
                f"Como queremos que tu festejo sea bien *ta'ipa* y dulce, hoy te tenemos un regalito para que acompañes tu cafecito:\n\n"
                f"🎁 *¡Hoy te invitamos un Muffin de arándanos totalmente gratis!* 🧁✨"
            )
            
            # Usamos la misma función que ya tienes configurada para Evolution API
            enviar_whatsapp_canje(nombre, celular, mensaje)
    else:
        print("☕ No hay cumpleañeros hoy.", flush=True)

    return {"status": "success", "message": f"Campaña finalizada. {len(encontrados)} mensajes enviados."}, 200