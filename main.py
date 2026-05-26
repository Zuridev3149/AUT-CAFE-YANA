import requests
import traceback
from flask import Flask, jsonify

# Importamos las lógicas de nuestros sub-archivos
from logica_fidelizacion import procesar_canjes_tradicionales
from logica_promos import procesar_canjes_promocionales
from logica_cumpleanos import procesar_cumpleanos  # <--- NUEVA LÍNEA
from logica_temporada import procesar_promos_temporada  # <--- NUEVA LÍNEA

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DE AZURE
# ==========================================
BASE_URL = "https://kafeyanaapi20260321224446-bqdjh9acame8gydt.centralus-01.azurewebsites.net"
LOGIN_URL = f"{BASE_URL}/api/Aunth/Login"
GRAPHQL_URL = f"{BASE_URL}/graphql/"

CREDENTIALS = {
    "email": "admin@gmail.com",
    "password": "Admin123#"
}

sesion = requests.Session()

def iniciar_sesion():
    print("🔐 Iniciando sesión en Azure...", flush=True)
    try:
        response = sesion.post(LOGIN_URL, json=CREDENTIALS)
        response.raise_for_status()

        datos_login = response.json()
        token = datos_login.get("token") or datos_login.get("accessToken") or datos_login.get("jwt")

        if token:
            sesion.headers.update({"Authorization": f"Bearer {token}"})
            print("✅ Token JWT guardado en los encabezados.", flush=True)
        else:
            print("ℹ️ Sin Token explícito. Se usarán cookies de sesión HTTP.", flush=True)

        print("✅ Autenticación exitosa.\n", flush=True)
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al autenticar en Azure: {e}", flush=True)
        return False


# ==========================================
# RUTAS DE LOS WEBHOOKS
# ==========================================

@app.route('/webhook/venta', methods=['POST'])
def endpoint_venta():
    try:
        respuesta, status_code = procesar_canjes_tradicionales(sesion, GRAPHQL_URL)
        return jsonify(respuesta), status_code
    except Exception as e:
        print("❌ CRASH INTERNO EN EL WEBHOOK /venta:", flush=True)
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/webhook/productospermanentes', methods=['POST'])
def endpoint_productospermanentes():
    try:
        respuesta, status_code = procesar_canjes_promocionales(sesion, GRAPHQL_URL)
        return jsonify(respuesta), status_code
    except Exception as e:
        print("❌ CRASH INTERNO EN EL WEBHOOK /productospermanentes:", flush=True)
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500
    
@app.route('/webhook/cumpleanos', methods=['POST'])
def endpoint_cumpleanos():
    try:
        respuesta, status_code = procesar_cumpleanos(sesion, GRAPHQL_URL)
        return jsonify(respuesta), status_code
    except Exception as e:
        print("❌ CRASH INTERNO EN EL WEBHOOK /cumpleanos:", flush=True)
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500
    
@app.route('/webhook/temporada', methods=['POST'])
def endpoint_temporada():
    try:
        respuesta, status_code = procesar_promos_temporada(sesion, GRAPHQL_URL)
        return jsonify(respuesta), status_code
    except Exception as e:
        print("❌ CRASH INTERNO EN EL WEBHOOK /temporada:", flush=True)
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500


# ==========================================
# EJECUCIÓN DEL SERVIDOR
# ==========================================
if __name__ == "__main__":
    if iniciar_sesion():
        print("🚀 Servidor Yana Webhooks activo en el puerto 5000...", flush=True)
        app.run(host="0.0.0.0", port=5000, debug=True)