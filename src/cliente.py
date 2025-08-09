from .utils import cargar_datos, guardar_datos,registrar_venta
from .admin import mostrar_productos

def comprar_productos(ruta):
    productos = cargar_datos(ruta)
    carrito = []
    total = 0
    
    while True:
        mostrar_productos(ruta)

        try:
            id_producto = int(input("\nIngrese el ID del producto que desea comprar (0 para salir): "))
        except ValueError:
            print("Ingrese un número válido")
            continue

        if id_producto == 0:
            break

        producto = next((p for p in productos if p["id"] == id_producto), None)
        if not producto:
            print("Producto no encontrado")
            continue

        try:
            cantidad = int(input(f"Ingrese la cantidad de '{producto['nombre']}' que desea comprar: "))
        except ValueError:
            print("Cantidad inválida")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0.")
        elif cantidad > producto["stock"]:
            print(f"Solo hay {producto['stock']} unidades disponibles.")
        else:
            subtotal = round(cantidad * producto["precio"], 2)
            producto["stock"] -= cantidad
            carrito.append({
                "nombre": producto["nombre"],
                "cantidad": cantidad,
                "precio": producto["precio"],
                "sub_total": subtotal
            })
            total += subtotal
            print(f"{cantidad} unidades de {producto['nombre']} agregadas al carrito")
   

    # Guardar cambios en el JSON
    guardar_datos(ruta,productos)

    print("\n🛒 Resumen de compra:")
    for item in carrito:
        print(f"- {item['cantidad']} x {item['nombre']} @ S/.{item['precio']} = S/.{item['sub_total']}")
    print(f"💰 Total a pagar: S/.{total:.2f}")

    if carrito:
        confirmar = input("\n¿Desea confirmar la compra? (s/n): ").strip().lower()
        if confirmar == "s":
            registrar_venta(carrito, total, "data/ventas.json")
            print("✅ ¡Compra realizada con éxito!")
        else:
            print("❌ Compra cancelada.")
    