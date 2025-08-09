import tkinter as tk
from tkinter import messagebox

# Importamos las clases GUI que ya tienes creadas
from admin_gui import AdminApp
from cliente_gui import ClienteApp

class MainApp:
    def __init__(self, master):
        self.master = master
        master.title("Tienda Virtual - Menú Principal")
        master.geometry("300x150")

        label = tk.Label(master, text="Selecciona un modo:", font=("Arial", 14))
        label.pack(pady=20)

        btn_admin = tk.Button(master, text="Administrador", width=20, command=self.abrir_admin)
        btn_admin.pack(pady=5)

        btn_cliente = tk.Button(master, text="Cliente", width=20, command=self.abrir_cliente)
        btn_cliente.pack(pady=5)

    def abrir_admin(self):
        self.master.withdraw()  # Oculta ventana principal
        admin_window = tk.Toplevel()
        app = AdminApp(admin_window)
        admin_window.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(admin_window))

    def abrir_cliente(self):
        self.master.withdraw()  # Oculta ventana principal
        cliente_window = tk.Toplevel()
        app = ClienteApp(cliente_window)
        cliente_window.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(cliente_window))

    def cerrar_ventana(self, ventana):
        ventana.destroy()
        self.master.deiconify()  # Muestra ventana principal de nuevo

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()