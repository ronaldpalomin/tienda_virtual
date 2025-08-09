import tkinter as tk
from tkinter import messagebox, simpledialog
from utils import cargar_datos, guardar_datos, registrar_venta

RUTA_JSON = "data/productos.json"
RUTA_VENTAS = "data/ventas.json"

class ClienteApp:
    def __init__(self, master):
        self.master = master
        master.title("Tienda Virtual - Cliente")
        master.geometry("600x400")

        self.productos = cargar_datos(RUTA_JSON)
        self.carrito = []
        self.total = 0

        # Lista de productos
        self.lista_productos = tk.Listbox(master, width=80)
        self.lista_productos.pack(pady=10)

        # Botones
        frame_botones = tk.Frame(master)
        frame_botones.pack()

        tk.Button(frame_botones, text="Agregar al carrito", command=self.agregar_al_carrito).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Mostrar carrito", command=self.mostrar_carrito).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Confirmar compra", command=self.confirmar_compra).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Actualizar productos", command=self.cargar_lista).grid(row=0, column=3, padx=5)

        self.cargar_lista()

    def cargar_lista(self):
        self.lista_productos.delete(0, tk.END)
        self.productos = cargar_datos(RUTA_JSON)
        for p in self.productos:
            self.lista_productos.insert(tk.END, f"{p['id']}: {p['nombre']} - S/.{p['precio']} (Stock: {p['stock']})")

    def agregar_al_carrito(self):
        seleccion = self.lista_productos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto para agregar al carrito.")
            return
        index = seleccion[0]
        producto = self.productos[index]

        try:
            cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad de '{producto['nombre']}' que desea comprar:", minvalue=1)
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return
        if cantidad is None:
            return  # Canceló el diálogo

        if cantidad > producto['stock']:
            messagebox.showerror("Error", f"Solo hay {producto['stock']} unidades disponibles.")
            return

        subtotal = round(cantidad * producto['precio'], 2)
        producto['stock'] -= cantidad
        self.carrito.append({
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio": producto["precio"],
            "sub_total": subtotal
        })
        self.total += subtotal

        messagebox.showinfo("Éxito", f"{cantidad} unidades de {producto['nombre']} agregadas al carrito.")
        self.cargar_lista()

    def mostrar_carrito(self):
        if not self.carrito:
            messagebox.showinfo("Carrito vacío", "No hay productos en el carrito.")
            return
        texto = ""
        for item in self.carrito:
            texto += f"{item['cantidad']} x {item['nombre']} @ S/.{item['precio']} = S/.{item['sub_total']}\n"
        texto += f"\nTotal: S/.{self.total:.2f}"
        messagebox.showinfo("Carrito de compras", texto)

    def confirmar_compra(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "No hay productos para comprar.")
            return
        confirmar = messagebox.askyesno("Confirmar compra", f"El total es S/.{self.total:.2f}. ¿Desea confirmar la compra?")
        if confirmar:
            registrar_venta(self.carrito, self.total, RUTA_VENTAS)
            guardar_datos(RUTA_JSON, self.productos)  # Guardar el stock actualizado
            messagebox.showinfo("Compra exitosa", "¡Compra realizada con éxito!")
            self.carrito.clear()
            self.total = 0
            self.cargar_lista()
        else:
            messagebox.showinfo("Compra cancelada", "Compra cancelada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()
