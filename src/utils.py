import json
import os
from datetime import datetime


def registrar_venta(carrito,total,ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            ventas = json.load(f)
    except FileNotFoundError:
        ventas = []

    nueva_venta = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": carrito,
        "total": total
    }

    ventas.append(nueva_venta)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(ventas, f, ensure_ascii=False, indent=4)

    print("✅ Venta registrada correctamente")


def cargar_datos(ruta):
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(ruta,datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    