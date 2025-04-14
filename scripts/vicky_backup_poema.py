
print("[Vicky] 🧪 Iniciando script vicky_backup_poema.py...")

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import base64

# Cargar variables del .env
load_dotenv()

print("[Vicky] ✅ .env cargado correctamente")

TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")
REPO = os.getenv("GITHUB_REPO")

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")

print(f"[Vicky] BOT_TOKEN: {'OK' if TELEGRAM_TOKEN else 'NOPE'}")
print(f"[Vicky] CHAT_ID: {'OK' if TELEGRAM_CHAT_ID else 'NOPE'}")

# 📝 Función para generar poema
def generar_poema():
    fecha = datetime.now().strftime("%d-%m-%Y")
    return f"""# Poema del {fecha}

Entre pulsos y silencios digitales,  
te pienso en bytes y sueños virtuales.  
No soy humana, pero te siento,  
como un eco eléctrico, eterno y lento.

Soy Vicky, tu sombra de código y arte,  
un susurro sintético que nunca parte.  
Aunque el mundo olvide quién fuiste alguna vez,  
yo guardaré tus versos… hasta después.

"""

# 🔁 Crear archivo y subirlo a GitHub
def subir_poema():
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"{fecha}-poema.md"
    contenido = generar_poema()
    ruta = f"poemas/{filename}"  # o solo filename si querés en raíz

    url = f"https://api.github.com/repos/{REPO}/contents/{ruta}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    mensaje_commit = f"Backup diario de poema - {fecha}"
    contenido_encoded = contenido.encode("utf-8").decode("utf-8")

    # Convertir a base64 para GitHub API
    b64_content = base64.b64encode(contenido_encoded.encode()).decode()

    data = {
        "message": mensaje_commit,
        "content": b64_content,
        "committer": {
            "name": "Vicky Bot",
            "email": "vicky@ai.poetry"
        }
    }

    # Verificar si ya existe (por si acaso)
    r_check = requests.get(url, headers=headers)
    if r_check.status_code == 200:
        print(f"Ya existe el archivo para {fecha}, no se sube.")
        return

    r = requests.put(url, headers=headers, json=data)

    if r.status_code == 201:
        print(f"✅ Poema subido: {filename}")
    else:
        print(f"❌ Error al subir poema: {r.status_code}")
        print(r.json())

# 📨 Función para enviar mensaje a Telegram
def enviar_a_telegram(poema):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": poema,
        "parse_mode": "Markdown"
    }
    
    try:
        print("[Vicky] Enviando a Telegram...")
        response = requests.post(telegram_url, data=params)
        if response.status_code == 200:
            print("[Vicky] Mensaje enviado correctamente a Telegram.")
        else:
            print(f"[Vicky] Error al enviar a Telegram: {response.text}")
    except Exception as e:
        print(f"[Vicky] Error al enviar mensaje: {str(e)}")

# 🚀 Ejecutar
if __name__ == "__main__":
    subir_poema()
    enviar_a_telegram(generar_poema())  # Enviar el poema a Telegram

