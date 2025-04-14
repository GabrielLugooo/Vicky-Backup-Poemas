# convert_poemas.py

import os
import json
from datetime import datetime

POEMAS_DIR = "poemas"
OUTPUT_JSON = "poemas.json"

def cargar_poemas():
    poemas = []

    for filename in sorted(os.listdir(POEMAS_DIR)):
        if filename.endswith(".md"):
            path = os.path.join(POEMAS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read()

            titulo = filename.replace(".md", "")
            poemas.append({
                "title": f"Poema del {titulo}",
                "content": contenido.strip()
            })

    return poemas

def guardar_json(poemas):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(poemas, f, ensure_ascii=False, indent=2)
    print(f"✅ Se generó {OUTPUT_JSON} con {len(poemas)} poemas.")

if __name__ == "__main__":
    poemas = cargar_poemas()
    guardar_json(poemas)
