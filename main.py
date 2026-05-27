import requests
import traceback
import sys
from flask import Flask, jsonify, request
import urllib3

# Importamos las lógicas de nuestros sub-archivos
from logica_fidelizacion import procesar_canjes_tradicionales
from logica_promos import procesar_canjes_promocionales
from logica_cumpleanos import procesar_cumpleanos
from logica_temporada import procesar_promos_temporada

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN LOCAL / DESARROLLO
# ==========================================
BASE_URL = "http://host.docker.internal:5012"
LOGIN_URL = f"{BASE_URL}/api/Aunth/Login"
GRAPHQL_URL = f"{BASE_URL}/graphql/"

CREDENTIALS = {
    "email": "soporte@gmail.com",
    "password": "password"
}

sesion = requests.Session()

sesion.mount("http://", requests.adapters.HTTPAdapter(max_retries=1))
_original_post = sesion.post
sesion.post = lambda *args, **kwargs: _original_post(*args, timeout=kwargs.pop('timeout', 10), **kwargs)

sesion.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def iniciar_sesion():
    print(f"🔐 Iniciando sesión en backend local ({BASE_URL})...", flush=True)
    try:
        response = sesion.post(LOGIN_URL, json=CREDENTIALS, timeout=5)
        response.raise_for_status()

        datos_login = response.json() or {}
        token = datos_login.get("token") or datos_login.get("accessToken") or datos_login.get("jwt")

        if token:
            sesion.headers.update({"Authorization": f"Bearer {token}"})
            print("✅ Token JWT guardado en los encabezados locales.", flush=True)
        else:
            print("ℹ️ Sin Token explícito. Se usarán cookies de sesión HTTP.", flush=True)

        print("✅ Autenticación exitosa con tu .NET local.\n", flush=True)
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al autenticar en el .NET local: {e}", flush=True)
        return False


# ==========================================
# HELPER DE DIAGNÓSTICO
# ==========================================
def log_flush(*args):
    print(*args, flush=True)
    sys.stdout.flush()
    sys.stderr.flush()


# ==========================================
# RUTAS DE LOS WEBHOOKS
# ==========================================

@app.route('/webhook/venta', methods=['POST'])
def endpoint_venta():
    log_flush("=" * 60)
    log_flush("📥 [VENTA] Webhook recibido")
    log_flush(f"   Headers: {dict(request.headers)}")
    log_flush(f"   Body raw: {request.get_data()}")
    log_flush("=" * 60)

    try:
        log_flush("🔄 [VENTA] Llamando a procesar_canjes_tradicionales()...")
        resultado = procesar_canjes_tradicionales(sesion, GRAPHQL_URL)
        log_flush(f"✅ [VENTA] Resultado recibido: {resultado}")

        if resultado is None:
            log_flush("⚠️ [VENTA] La función devolvió None")
            return jsonify({"status": "error", "error": "La función devolvió None (GraphQL vacío)"}), 500

        if not isinstance(resultado, tuple) or len(resultado) != 2:
            log_flush(f"⚠️ [VENTA] Resultado con formato inesperado: tipo={type(resultado)}, valor={resultado}")
            return jsonify({"status": "error", "error": f"Formato de respuesta inesperado: {type(resultado)}"}), 500

        respuesta, status_code = resultado
        log_flush(f"✅ [VENTA] Respondiendo con status {status_code}: {respuesta}")
        return jsonify(respuesta), status_code

    except Exception as e:
        log_flush("❌ [VENTA] CRASH INTERNO:")
        log_flush(f"   Tipo de error : {type(e).__name__}")
        log_flush(f"   Mensaje       : {str(e)}")
        log_flush("   Traceback completo:")
        traceback.print_exc(file=sys.stdout)
        sys.stdout.flush()
        return jsonify({
            "status": "error",
            "error": str(e),
            "tipo": type(e).__name__,
            "traceback": traceback.format_exc()  # 👈 también lo devuelve en la respuesta HTTP
        }), 500


@app.route('/webhook/productospermanentes', methods=['POST'])
def endpoint_productospermanentes():
    log_flush("=" * 60)
    log_flush("📥 [PERMANENTES] Webhook recibido")
    log_flush(f"   Headers: {dict(request.headers)}")
    log_flush(f"   Body raw: {request.get_data()}")
    log_flush("=" * 60)

    try:
        log_flush("🔄 [PERMANENTES] Llamando a procesar_canjes_promocionales()...")
        resultado = procesar_canjes_promocionales(sesion, GRAPHQL_URL)
        log_flush(f"✅ [PERMANENTES] Resultado recibido: {resultado}")

        if resultado is None:
            log_flush("⚠️ [PERMANENTES] La función devolvió None")
            return jsonify({"status": "error", "error": "La función devolvió None (GraphQL vacío)"}), 500

        if not isinstance(resultado, tuple) or len(resultado) != 2:
            log_flush(f"⚠️ [PERMANENTES] Resultado con formato inesperado: tipo={type(resultado)}, valor={resultado}")
            return jsonify({"status": "error", "error": f"Formato de respuesta inesperado: {type(resultado)}"}), 500

        respuesta, status_code = resultado
        log_flush(f"✅ [PERMANENTES] Respondiendo con status {status_code}: {respuesta}")
        return jsonify(respuesta), status_code

    except Exception as e:
        log_flush("❌ [PERMANENTES] CRASH INTERNO:")
        log_flush(f"   Tipo de error : {type(e).__name__}")
        log_flush(f"   Mensaje       : {str(e)}")
        log_flush("   Traceback completo:")
        traceback.print_exc(file=sys.stdout)
        sys.stdout.flush()
        return jsonify({
            "status": "error",
            "error": str(e),
            "tipo": type(e).__name__,
            "traceback": traceback.format_exc()  # 👈 también lo devuelve en la respuesta HTTP
        }), 500


@app.route('/webhook/cumpleanos', methods=['POST'])
def endpoint_cumpleanos():
    try:
        resultado = procesar_cumpleanos(sesion, GRAPHQL_URL)
        if resultado is None:
            return jsonify({"status": "error", "error": "La función devolvió None (GraphQL vacío)"}), 500
        respuesta, status_code = resultado
        return jsonify(respuesta), status_code
    except Exception as e:
        print("❌ CRASH INTERNO EN EL WEBHOOK /cumpleanos:", flush=True)
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/webhook/temporada', methods=['POST'])
def endpoint_temporada():
    try:
        resultado = procesar_promos_temporada(sesion, GRAPHQL_URL)
        if resultado is None:
            return jsonify({"status": "error", "error": "La función devolvió None (GraphQL vacío)"}), 500
        respuesta, status_code = resultado
        return jsonify(respuesta), status_code
    except Exception as e:
        print("❌ CRASH INTERNO EN EL WEBHOOK /temporada:", flush=True)
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500


# ==========================================
# EJECUCIÓN DEL SERVIDOR
# ==========================================
if __name__ == "__main__":
    iniciar_sesion()
    print("🚀 Servidor Yana Webhooks activo en el puerto 5000...", flush=True)
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)