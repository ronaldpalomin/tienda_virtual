from utils import cargar_datos, guardar_datos

def agregar_productos(ruta):



    productos = cargar_datos(ruta)
    print("\n--- Agregar nuevo producto ---")
    nombre = input("Nombre del producto: ").lower()
    try:
        precio = float(input("Precio (S/.):"))
        stock = int(input("Stock disponible: "))
    
    except ValueError:
        print("Error : precio y stock deben ser numeros validos")
        return
    
#calcular el siguiente id automaticamente
    nuevo_id = max([p['id'] for p in productos], default = 0) + 1

    productos.append({
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
        "stock": stock
    })

    guardar_datos(ruta,productos)
    print(f"Producto '{nombre}' agregado con ID {nuevo_id}")

def mostrar_productos(ruta):
    productos = cargar_datos(ruta)
    if not productos:
        print("No hay productos disponibles. ")
        return
    print("\n📦 Lista de productos:")
    for p in productos:
        print(f"{p['id']}: {p['nombre']} - S/.{p['precio']} (Stock: {p['stock']})")


def modificar_productos(ruta):
    productos = cargar_datos(ruta)
    mostrar_productos(ruta)
    try:
        id_producto = int(input("\nIngrese el ID del producto a modificar: "))
    except ValueError:
        print("ID Invalido")
        return
    producto = next((p for p in productos if p["id"] == id_producto), None)
    if not producto:
        print("Producto no encontrado")
        return
    try:
        nuevo_precio = float(input(f"Nuevo precio de '{producto['nombre']}' (actual: S/. {producto['precio']}): "))
        nuevo_stock = int(input(f"Nuevo stock de '{producto['nombre']}' (actual: {producto['stock']}): "))
    except ValueError:
        print("Datos invalidos")
        return
    producto['precio']  = nuevo_precio
    producto['stock'] = nuevo_stock

    guardar_datos(ruta, productos)
    print(f"Producto '{producto['nombre']}' modificado correctamente")

def eliminar_productos(ruta):
    productos = cargar_datos(ruta)
    mostrar_productos(ruta)
    try:
        id_producto=int(input("\nIngrese el ID del producto a eliminar: "))
    except ValueError:
        print("ID INVALIDO")

    producto = next((p for p in productos if p["id"] == id_producto), None)
    if not producto:
        print("❌ Producto no encontrado.")
        return
    productos.remove(producto)
    guardar_datos(ruta,productos)
    print(f"✅ Producto '{producto['nombre']}' eliminado correctamente.")

def ver_ventas(ruta):
    vt = cargar_datos(ruta)
    print("\n📜 HISTORIAL DE VENTAS 📜")
    for venta in vt:
        print(f"\n🗓 {venta['fecha']}")
        for item in venta["items"]:
            print(f"   - {item['cantidad']} x {item['nombre']} @ S/.{item['precio']} = S/.{item['sub_total']}")
        print(f"💰 Total: S/.{venta['total']:.2f}")