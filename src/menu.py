from src.admin import agregar_productos, mostrar_productos, modificar_productos,eliminar_productos,ver_ventas
from src.cliente import comprar_productos

RUTA_JSON = "data/productos.json"
RUTA_VENTA = "data/ventas.json"

def menu_admin():
    while True:
                print("\n--- MENÚ ADMINISTRADOR ---")
                print("1. Agregar producto")
                print("2. Mostrar Productos")
                print("3. Modificar producto")
                print("4. Eliminar producto")
                print("5. Ver ventas")
                print("6. Volver al menú principal")

                admin_opcion = input("Seleccione una opcion: ")
                if admin_opcion == "1":
                    agregar_productos(RUTA_JSON)
                elif admin_opcion == "2":
                    mostrar_productos(RUTA_JSON)
                elif admin_opcion == "3":
                    modificar_productos(RUTA_JSON)
                elif admin_opcion == "4":
                    eliminar_productos(RUTA_JSON)
                elif admin_opcion == "5":
                    ver_ventas(RUTA_VENTA)
                    break
                elif admin_opcion == "6":
                    break
                else:
                    print("❌ Opción inválida.")

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Modo Cliente")
        print("2. Modo Administrador")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            comprar_productos(RUTA_JSON)
        if opcion == "2":
            menu_admin()

        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


