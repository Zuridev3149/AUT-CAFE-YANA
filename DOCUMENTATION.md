# ☕ Automatización y Fidelización - Cafetería Yana

Bienvenido al repositorio central de automatización de **Cafetería Yana**. Este ecosistema está diseñado con una arquitectura de microservicios usando Docker, Python (Flask), y conectando n8n con Evolution API para manejar flujos de marketing, cumpleaños y promociones estacionales por WhatsApp.

---

## 🏗️ 1. Arquitectura del Sistema

El sistema se compone de 4 microservicios orquestados mediante `docker-compose.yml`:

1. **db_yana (PostgreSQL):** Base de datos principal para Evolution API.
2. **n8n_yana:** Entorno para construir flujos visuales (puerto `5678`).
3. **evolution_api:** Wrapper oficial para la API de WhatsApp (puerto `8081` externo -> `8080` interno).
4. **cerebro_python:** Servidor Flask corriendo en `python:3.11-slim-bullseye`. Renderiza tarjetas HTML en Base64 de alta resolución usando `wkhtmltopdf` y `imgkit`, y coordina la lógica de negocio (puerto `5000`).

---

## 🚀 2. Guía de Despliegue

### 2.1 Requisitos Previos
* Docker y Docker Compose instalados.
* Git instalado y configurado.
* Consola de PowerShell (o Bash en Linux/Mac).

### 2.2 Levantar el Ecosistema
1. Clona el repositorio:
   ```bash
   git clone [https://github.com/Zuridev3149/Automatizaci-n-Kafe-Yana.git](https://github.com/Zuridev3149/Automatizaci-n-Kafe-Yana.git)
   cd Automatizaci-n-Kafe-Yana
   ```
2. Construye y levanta los contenedores en segundo plano:
   ```bash
   docker compose up -d --build
   ```
3. Verifica que el cerebro en Python esté corriendo y haya instalado sus dependencias (`wkhtmltopdf`):
   ```bash
   docker logs -f yana_python_bot
   ```

---

## 📱 3. Conexión a WhatsApp (Generación del QR)

Evolution API gestiona las sesiones de WhatsApp. Si es la primera vez que despliegas o se cerró la sesión de `Yana_Bot`, debes vincular tu número leyendo el código QR.

### Paso A: Crear la instancia (Solo si no existe)
Si la instancia "Yana_Bot" fue borrada, créala ejecutando esto en PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8081/instance/create" -Headers @{"apikey"="yana_secret_key", "Content-Type"="application/json"} -Body '{"instanceName": "Yana_Bot", "qrcode": true}'
```

### Paso B: Generar y mostrar el Código QR
Ejecuta el siguiente script en PowerShell. Esto consultará a Evolution API, extraerá la imagen del QR, la inyectará en un archivo `qr.html` centrado y lo abrirá en tu navegador:
```powershell
$res = Invoke-RestMethod -Method Get -Uri "http://localhost:8081/instance/connect/Yana_Bot" -Headers @{"apikey"="yana_secret_key"}
Set-Content -Path "qr.html" -Value "<body style='background:#1a1a1a;'><div style='display:flex; justify-content:center; align-items:center; height:100vh;'><img src='$($res.base64)' style='width:350px; background:white; padding:20px; border-radius:15px;'/></div></body>"
Start-Process "qr.html"
```
*💡 Nota: Escanea el QR rápidamente desde "Dispositivos Vinculados" en WhatsApp.*

---

## 🧠 4. Estructura del "Cerebro Python"

* **`main.py`:** Orquestador principal (Servidor Flask). Declara las rutas (webhooks).
* **`generador_tarjetas.py`:** Contiene las plantillas HTML/CSS. Usa `imgkit` para exportar a PNG en resolución 4K.
* **`whatsapp.py`:** Cliente HTTP para hablar con Evolution API (`/message/sendText` y `/message/sendMedia`).
* **Módulos de Lógica (`logica_cumpleanos.py`, `logica_temporada.py`):** Contienen consultas GraphQL a Azure y las reglas de distribución masiva.

---

## 🎯 5. API Reference: Consumo de Endpoints (Para Desarrolladores)

Los webhooks están diseñados para ser consumidos por cualquier servicio backend en **.NET**, tarea programada o herramienta de automatización. El servidor interno expone los servicios en `http://localhost:5000`.

**Formato general de respuesta exitosa (HTTP 200 OK):**
```json
{
  "status": "success",
  "message": "Procesamiento ejecutado: X mensajes enviados"
}
```

### 🎂 Endpoint 1: Promociones de Cumpleaños
Inicia el escaneo de clientes activos cuyo cumpleaños coincide con la fecha de hoy y les envía una tarjeta gráfica reclamando un Muffin de cortesía.

* **URL:** `/webhook/cumpleanos`
* **Método HTTP:** `POST`
* **Headers requeridos:** Ninguno por defecto.
* **Body:** Vacío.

#### Ejemplo de integración en C# (.NET):
```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace YanaBotIntegrations
{
    class Program
    {
        private static readonly HttpClient client = new HttpClient();

        static async Task Main(string[] args)
        {
            Console.WriteLine("Iniciando campaña de cumpleaños...");
            try
            {
                // Se envía POST sin contenido (null)
                HttpResponseMessage response = await client.PostAsync("http://localhost:5000/webhook/cumpleanos", null);
                response.EnsureSuccessStatusCode();
                
                string responseBody = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Respuesta del bot: {responseBody}");
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"❌ Error de conexión con el webhook: {e.Message}");
            }
        }
    }
}
```

---

### 🍂 Endpoint 2: Descuentos de Temporada
Consulta si existen temporadas activas (ej. "Invierno 2026"). Por **cada temporada vigente**, genera una tarjeta gráfica personalizada con un 10% de descuento y la envía a toda la base de clientes. *(Si hay 2 temporadas activas simultáneamente, procesará envíos individuales para cada una).*

* **URL:** `/webhook/temporada`
* **Método HTTP:** `POST`
* **Headers requeridos:** Ninguno por defecto.
* **Body:** Vacío.

#### Ejemplo de integración de clase estática en C# (.NET):
```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace YanaBotIntegrations
{
    public static class TemporadaManager
    {
        private static readonly HttpClient _httpClient = new HttpClient();

        public static async Task DispararTemporadaAsync()
        {
            try
            {
                Console.WriteLine("Detonando webhook de temporada en Yana Bot...");
                
                var response = await _httpClient.PostAsync("http://localhost:5000/webhook/temporada", null);
                response.EnsureSuccessStatusCode(); // Lanza excepción si no es 200 OK
                
                var result = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"✅ Campaña de temporada finalizada con éxito: {result}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Fallo al procesar la campaña de temporada: {ex.Message}");
            }
        }
    }
}
```

---

## 🛠️ 6. Mantenimiento y Actualizaciones

* **Aplicar cambios en Python:** Si modificas el diseño de una tarjeta (HTML/CSS) o la lógica en los `.py`, reinicia el bot para refrescar la memoria de Flask:
  ```bash
  docker restart yana_python_bot
  ```
* **Guardar progreso (Git):**
  Cada vez que el equipo de desarrollo agregue mejoras, sincronícenlo con el repo:
  ```bash
  git add .
  git commit -m "Descripción de las mejoras"
  git push
  ```

*☕ Desarrollado para escalar y brindar la mejor experiencia tecnológica en Cafetería Yana.*