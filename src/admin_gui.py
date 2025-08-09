import tkinter as tk
from tkinter import messagebox, simpledialog
from admin import agregar_productos, mostrar_productos, modificar_productos, eliminar_productos, ver_ventas
from utils import cargar_datos, guardar_datos

RUTA_JSON = "data/productos.json"
RUTA_VENTAS = "data/ventas.json"

class AdminApp:
    def __init__(self, master):
        self.master = master
        master.title("Panel de Administración")
        master.geometry("600x400")

        # Lista de productos
        self.lista_productos = tk.Listbox(master, width=80)
        self.lista_productos.pack(pady=10)

        # Botones para acciones
        frame_botones = tk.Frame(master)
        frame_botones.pack()

        tk.Button(frame_botones, text="Agregar Producto", command=self.agregar_producto).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Modificar Producto", command=self.modificar_producto).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar Producto", command=self.eliminar_producto).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Ver Ventas", command=self.ver_ventas).grid(row=0, column=3, padx=5)
        tk.Button(frame_botones, text="Actualizar Lista", command=self.cargar_lista).grid(row=0, column=4, padx=5)

        self.cargar_lista()

    def cargar_lista(self):
        self.lista_productos.delete(0, tk.END)
        self.productos = cargar_datos(RUTA_JSON)
        for p in self.productos:
            self.lista_productos.insert(tk.END, f"{p['id']}: {p['nombre']} - S/.{p['precio']} (Stock: {p['stock']})")

    def agregar_producto(self):
        # Pedir datos con simpledialog
        nombre = simpledialog.askstring("Agregar Producto", "Nombre del producto:").lower()
        if not nombre:
            return
        try:
            precio = float(simpledialog.askstring("Agregar Producto", "Precio (S/.):"))
            stock = int(simpledialog.askstring("Agregar Producto", "Stock disponible:"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Precio y stock deben ser números válidos")
            return

        # Calcular nuevo id
        nuevo_id = max([p['id'] for p in self.productos], default=0) + 1
        self.productos.append({"id": nuevo_id, "nombre": nombre, "precio": precio, "stock": stock})
        guardar_datos(RUTA_JSON, self.productos)
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado con ID {nuevo_id}")
        self.cargar_lista()

    def modificar_producto(self):
        seleccion = self.lista_productos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para modificar")
            return
        index = seleccion[0]
        producto = self.productos[index]

        try:
            nuevo_precio = float(simpledialog.askstring("Modificar Producto", f"Nuevo precio de '{producto['nombre']}' (actual: S/. {producto['precio']}):"))
            nuevo_stock = int(simpledialog.askstring("Modificar Producto", f"Nuevo stock de '{producto['nombre']}' (actual: {producto['stock']}):"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Datos inválidos")
            return

        producto['precio'] = nuevo_precio
        producto['stock'] = nuevo_stock
        guardar_datos(RUTA_JSON, self.productos)
        messagebox.showinfo("Éxito", f"Producto '{producto['nombre']}' modificado correctamente")
        self.cargar_lista()

    def eliminar_producto(self):
        seleccion = self.lista_productos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        index = seleccion[0]
        producto = self.productos[index]

        if messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que quiere eliminar '{producto['nombre']}'?"):
            self.productos.remove(producto)
            guardar_datos(RUTA_JSON, self.productos)
            messagebox.showinfo("Éxito", f"Producto '{producto['nombre']}' eliminado correctamente")
            self.cargar_lista()

    def ver_ventas(self):
        ventas = cargar_datos(RUTA_VENTAS)
        texto = ""
        for venta in ventas:
            texto += f"\nFecha: {venta['fecha']}\n"
            for item in venta["items"]:
                texto += f"  - {item['cantidad']} x {item['nombre']} @ S/.{item['precio']} = S/.{item['sub_total']}\n"
            texto += f"Total: S/.{venta['total']:.2f}\n"
            texto += "-"*30

        if texto == "":
            texto = "No hay ventas registradas."
        # Mostrar en ventana nueva
        ventana_ventas = tk.Toplevel(self.master)
        ventana_ventas.title("Historial de Ventas")
        ventana_ventas.geometry("400x300")
        txt = tk.Text(ventana_ventas)
        txt.pack(expand=True, fill='both')
        txt.insert(tk.END, texto)
        txt.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()
