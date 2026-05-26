import base64
import imgkit

def generar_tarjeta_base64(nombre_cliente):
    """Toma la plantilla HTML, inyecta el nombre y la convierte a imagen Base64"""
    
    # 💡 Usamos .upper() para que el nombre siempre salga en MAYÚSCULAS como en el diseño
    nombre_formateado = str(nombre_cliente).strip().upper()

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Kafe Yana – ¡Feliz Cumpleaños!</title>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --brown-dark:   #3b1e1e;
      --brown-card:   #4a2020;
      --brown-medium: #5c2a2a;
      --gold:         #c9a84c;
      --gold-light:   #e2c97e;
      --cream:        #f5ead4;
      --green:        #6b8f5e;
      --green-light:  #8aad7a;
    }}

    body {{
      background: var(--brown-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: 'Lato', sans-serif;
    }}

    .card {{
      width: 400px;
      height: 460px;
      background: var(--brown-card);
      border: 3px solid var(--gold);
      border-radius: 6px;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 22px 28px 20px;
      overflow: hidden;
    }}

    .bunting {{
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 30px;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      gap: 0;
    }}
    .bunting::before,
    .bunting::after {{
      content: '';
      position: absolute;
      top: 4px;
      left: 10%; right: 10%;
      border-top: 1.5px solid var(--green);
    }}
    .flag {{
      width: 0;
      height: 0;
      border-left:  10px solid transparent;
      border-right: 10px solid transparent;
      border-top:   16px solid var(--green);
      margin: 0 2px;
    }}
    .flag:nth-child(odd)  {{ border-top-color: var(--green); }}
    .flag:nth-child(even) {{ border-top-color: var(--green-light); }}

    .top {{ display: flex; flex-direction: column; align-items: center; margin-top: 18px; gap: 6px; }}

    .steam-wrap {{ display: flex; gap: 7px; height: 22px; align-items: flex-end; }}
    .steam {{ width: 3px; border-radius: 2px; background: var(--cream); opacity: .55; }}
    .steam:nth-child(1) {{ height: 14px; }}
    .steam:nth-child(2) {{ height: 20px; }}
    .steam:nth-child(3) {{ height: 12px; }}

    .cup-svg {{ width: 72px; height: 58px; }}

    .brand-name {{
      font-family: 'Cinzel', serif;
      color: var(--cream);
      font-size: 1.25rem;
      letter-spacing: .12em;
      font-weight: 700;
      text-shadow: 0 1px 3px rgba(0,0,0,.4);
    }}

    .birthday-box {{
      width: 100%;
      border: 1.5px solid var(--gold);
      border-radius: 4px;
      padding: 10px 16px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      position: relative;
    }}
    .birthday-box::before,
    .birthday-box::after {{
      content: '✦';
      position: absolute;
      color: var(--gold);
      font-size: .55rem;
      top: 50%; transform: translateY(-50%);
    }}
    .birthday-box::before {{ left: 8px; }}
    .birthday-box::after  {{ right: 8px; }}

    .feliz {{ font-family: 'Cinzel', serif; font-size: .62rem; letter-spacing: .32em; color: var(--gold-light); text-transform: uppercase; }}

    .name {{
      font-family: 'Cinzel', serif;
      font-size: 2.4rem;
      font-weight: 900;
      letter-spacing: .35em;
      color: var(--cream);
      line-height: 1;
      text-shadow: 0 2px 8px rgba(0,0,0,.5);
    }}

    .regalo {{
      width: 100%; margin-top: 8px; border-top: 1px dashed rgba(201,168,76,.4);
      padding-top: 8px; display: flex; flex-direction: column; align-items: center; gap: 3px;
    }}
    .regalo-label {{ font-family: 'Lato', sans-serif; font-size: .58rem; font-weight: 300; letter-spacing: .18em; color: var(--gold-light); text-transform: uppercase; opacity: .8; }}
    .regalo-producto {{ font-family: 'Cinzel', serif; font-size: .85rem; font-weight: 700; color: var(--cream); letter-spacing: .08em; text-align: center; }}
    .regalo-emoji {{ font-size: 1.1rem; }}

    .beans-row {{ display: flex; align-items: center; justify-content: center; gap: 80px; width: 100%; opacity: .75; }}
    .bean {{ width: 26px; height: 16px; }}

    .bottom {{ display: flex; flex-direction: column; align-items: center; gap: 2px; padding-bottom: 4px; }}
    .con-amor {{ font-family: 'Lato', sans-serif; font-size: .65rem; font-weight: 300; color: var(--cream); letter-spacing: .1em; opacity: .8; }}
    .brand-bottom {{ font-family: 'Cinzel', serif; font-size: .8rem; color: var(--gold-light); letter-spacing: .12em; font-weight: 700; }}
  </style>
</head>
<body>
<div class="card">
  <div class="bunting">
    <div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div>
  </div>
  <div class="top">
    <div class="steam-wrap"><div class="steam"></div><div class="steam"></div><div class="steam"></div></div>
    <svg class="cup-svg" viewBox="0 0 72 58" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="36" cy="52" rx="30" ry="5" stroke="#f5ead4" stroke-width="1.5" fill="none"/>
      <path d="M14 24 L18 48 H54 L58 24 Z" stroke="#f5ead4" stroke-width="1.5" fill="none" stroke-linejoin="round"/>
      <ellipse cx="36" cy="24" rx="22" ry="4" stroke="#f5ead4" stroke-width="1.5" fill="none"/>
      <path d="M58 30 Q72 30 72 38 Q72 46 58 44" stroke="#f5ead4" stroke-width="1.5" fill="none"/>
    </svg>
    <span class="brand-name">Kafe Yana</span>
  </div>
  <div class="birthday-box">
    <span class="feliz">¡Feliz Cumpleaños!</span>
    <span class="name">{nombre_formateado}</span>
    <div class="regalo">
      <span class="regalo-label">🎁 tu regalo de cortesía</span>
      <span class="regalo-emoji">☕</span>
      <span class="regalo-producto">1 Café Gratis</span>
      <span class="regalo-label">válido solo hoy · canjeable en tienda</span>
    </div>
  </div>
  <div class="beans-row">
    <svg class="bean" viewBox="0 0 26 16" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="13" cy="8" rx="12" ry="7" fill="#6b4226" stroke="#c9a84c" stroke-width="1"/><path d="M13 2 Q10 8 13 14" stroke="#c9a84c" stroke-width="1" fill="none"/></svg>
    <svg class="bean" viewBox="0 0 26 16" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="13" cy="8" rx="12" ry="7" fill="#6b4226" stroke="#c9a84c" stroke-width="1"/><path d="M13 2 Q16 8 13 14" stroke="#c9a84c" stroke-width="1" fill="none"/></svg>
  </div>
  <div class="bottom">
    <span class="con-amor">con amor de toda la familia</span>
    <span class="brand-bottom">Kafe Yana</span>
  </div>
</div>
</body>
</html>"""

    # Configuraciones para renderizar la imagen web
    # opciones = {
    #     'format': 'jpg',
    #     'quality': 100,
    #     'width': 420,
    #     'encoding': "UTF-8",
    #     'quiet': ''
    # }
# Configuraciones para renderizar la imagen web en Alta Definición
    opciones = {
        'format': 'png',            # 1. PNG hace que los textos y vectores SVG sean perfectos
        'width': 400,               # 2. Forzamos el ancho exacto de tu clase .card (400px)
        'zoom': 3,                  # 3. LA MAGIA: Renderiza la tarjeta al triple de tamaño
        'disable-smart-width': '',  # 4. Evita que Linux intente achicar la imagen
        'encoding': "UTF-8",
        'quiet': ''
    }

    try:
        imagen_bytes = imgkit.from_string(html_content, False, options=opciones)
        imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
        return imagen_base64
    except Exception as e:
        print(f"❌ Error al generar la imagen para {nombre_formateado}: {e}", flush=True)
        return None
      
def generar_tarjeta_temporada_base64(nombre_cliente, nombre_temporada):
    """Genera una tarjeta promocional de temporada con 10% de descuento en Base64"""
    
    nombre_formateado = str(nombre_cliente).strip().upper()
    temporada_formateada = str(nombre_temporada).strip().upper()

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Kafe Yana – ¡Promo Temporada!</title>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --brown-dark:   #3b1e1e;
      --brown-card:   #4a2020;
      --gold:         #c9a84c;
      --gold-light:   #e2c97e;
      --cream:        #f5ead4;
      --orange:       #c96f4c;
      --orange-light: #e28e7e;
    }}

    body {{ background: var(--brown-dark); display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: 'Lato', sans-serif; }}

    .card {{
      width: 400px; height: 460px; background: var(--brown-card);
      border: 3px solid var(--gold); border-radius: 6px; position: relative;
      display: flex; flex-direction: column; align-items: center; justify-content: space-between;
      padding: 22px 28px 20px; overflow: hidden;
    }}

    .bunting {{ position: absolute; top: 0; left: 0; right: 0; height: 30px; display: flex; align-items: flex-start; justify-content: center; gap: 0; }}
    .bunting::before, .bunting::after {{ content: ''; position: absolute; top: 4px; left: 10%; right: 10%; border-top: 1.5px solid var(--orange); }}
    .flag {{ width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-top: 16px solid var(--orange); margin: 0 2px; }}
    .flag:nth-child(odd)  {{ border-top-color: var(--orange); }}
    .flag:nth-child(even) {{ border-top-color: var(--orange-light); }}

    .top {{ display: flex; flex-direction: column; align-items: center; margin-top: 18px; gap: 6px; }}
    .steam-wrap {{ display: flex; gap: 7px; height: 22px; align-items: flex-end; }}
    .steam {{ width: 3px; border-radius: 2px; background: var(--cream); opacity: .55; }}
    .steam:nth-child(1) {{ height: 14px; }} .steam:nth-child(2) {{ height: 20px; }} .steam:nth-child(3) {{ height: 12px; }}
    .cup-svg {{ width: 72px; height: 58px; }}

    .brand-name {{ font-family: 'Cinzel', serif; color: var(--cream); font-size: 1.25rem; letter-spacing: .12em; font-weight: 700; text-shadow: 0 1px 3px rgba(0,0,0,.4); }}

    .promo-box {{
      width: 100%; border: 1.5px solid var(--gold); border-radius: 4px;
      padding: 10px 16px 12px; display: flex; flex-direction: column; align-items: center; gap: 4px; position: relative;
    }}
    .promo-box::before, .promo-box::after {{ content: '✦'; position: absolute; color: var(--gold); font-size: .55rem; top: 50%; transform: translateY(-50%); }}
    .promo-box::before {{ left: 8px; }} .promo-box::after {{ right: 8px; }}

    .subtitulo {{ font-family: 'Cinzel', serif; font-size: .62rem; letter-spacing: .32em; color: var(--gold-light); text-transform: uppercase; text-align: center; }}
    
    .temporada {{ font-family: 'Cinzel', serif; font-size: 1.6rem; font-weight: 900; letter-spacing: .15em; color: var(--cream); line-height: 1.2; text-shadow: 0 2px 8px rgba(0,0,0,.5); text-align: center; }}

    .descuento-box {{ width: 100%; margin-top: 8px; border-top: 1px dashed rgba(201,168,76,.4); padding-top: 8px; display: flex; flex-direction: column; align-items: center; gap: 2px; }}
    .descuento-numero {{ font-family: 'Cinzel', serif; font-size: 2.2rem; font-weight: 900; color: var(--gold-light); letter-spacing: .05em; line-height: 1; }}
    .descuento-label {{ font-family: 'Lato', sans-serif; font-size: .65rem; font-weight: 400; letter-spacing: .18em; color: var(--cream); text-transform: uppercase; margin-bottom: 5px; }}
    .cliente-label {{ font-family: 'Lato', sans-serif; font-size: .55rem; font-weight: 300; letter-spacing: .1em; color: var(--orange-light); text-transform: uppercase; }}

    .beans-row {{ display: flex; align-items: center; justify-content: center; gap: 80px; width: 100%; opacity: .75; }}
    .bean {{ width: 26px; height: 16px; }}
    .bottom {{ display: flex; flex-direction: column; align-items: center; gap: 2px; padding-bottom: 4px; }}
    .con-amor {{ font-family: 'Lato', sans-serif; font-size: .65rem; font-weight: 300; color: var(--cream); letter-spacing: .1em; opacity: .8; }}
    .brand-bottom {{ font-family: 'Cinzel', serif; font-size: .8rem; color: var(--gold-light); letter-spacing: .12em; font-weight: 700; }}
  </style>
</head>
<body>
<div class="card">
  <div class="bunting">
    <div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div><div class="flag"></div>
  </div>
  <div class="top">
    <div class="steam-wrap"><div class="steam"></div><div class="steam"></div><div class="steam"></div></div>
    <svg class="cup-svg" viewBox="0 0 72 58" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="36" cy="52" rx="30" ry="5" stroke="#f5ead4" stroke-width="1.5" fill="none"/>
      <path d="M14 24 L18 48 H54 L58 24 Z" stroke="#f5ead4" stroke-width="1.5" fill="none" stroke-linejoin="round"/>
      <ellipse cx="36" cy="24" rx="22" ry="4" stroke="#f5ead4" stroke-width="1.5" fill="none"/>
      <path d="M58 30 Q72 30 72 38 Q72 46 58 44" stroke="#f5ead4" stroke-width="1.5" fill="none"/>
    </svg>
    <span class="brand-name">Kafe Yana</span>
  </div>
  
  <div class="promo-box">
    <span class="subtitulo">¡Especial de Temporada!</span>
    <span class="temporada">{temporada_formateada}</span>
    <div class="descuento-box">
      <span class="descuento-numero">10% DTO</span>
      <span class="descuento-label">en todas tus compras</span>
      <span class="cliente-label">Exclusivo para: {nombre_formateado}</span>
    </div>
  </div>

  <div class="beans-row">
    <svg class="bean" viewBox="0 0 26 16" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="13" cy="8" rx="12" ry="7" fill="#c96f4c" stroke="#c9a84c" stroke-width="1"/><path d="M13 2 Q10 8 13 14" stroke="#c9a84c" stroke-width="1" fill="none"/></svg>
    <svg class="bean" viewBox="0 0 26 16" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="13" cy="8" rx="12" ry="7" fill="#c96f4c" stroke="#c9a84c" stroke-width="1"/><path d="M13 2 Q16 8 13 14" stroke="#c9a84c" stroke-width="1" fill="none"/></svg>
  </div>
  <div class="bottom">
    <span class="con-amor">por tiempo limitado</span>
    <span class="brand-bottom">Kafe Yana</span>
  </div>
</div>
</body>
</html>"""

    # Configuraciones 4K sin DPI
    opciones = {
        'format': 'png',
        'width': 400,
        'zoom': 3,
        'disable-smart-width': '',
        'encoding': "UTF-8",
        'quiet': ''
    }

    try:
        imagen_bytes = imgkit.from_string(html_content, False, options=opciones)
        return base64.b64encode(imagen_bytes).decode('utf-8')
    except Exception as e:
        print(f"❌ Error al generar la imagen de temporada para {nombre_formateado}: {e}", flush=True)
        return None