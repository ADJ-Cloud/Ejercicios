import tkinter as tk
from tkinter import Button, messagebox, simpledialog, Toplevel, Label, Entry, StringVar
import json
import os
from datetime import datetime
from tkinter import ttk

## dani martin saiz realizo este programa ##

# USUARIOS
usuarios_registrados = {
    '1010': 'Dani el Mejoh AB',
    '1234554321': 'ADMIN',
}

# JSON GUARDAR
archivo_pedidos = 'pedidos.json'

# VERIFICAR USUARIO
def verificar_usuario(codigo):
    return codigo in usuarios_registrados

# GUARDAR PEDIDO
def guardar_pedido(pedido):
    if os.path.exists(archivo_pedidos):
        with open(archivo_pedidos, 'r') as file:
            pedidos = json.load(file)
    else:
        pedidos = {}
    
    codigo_usuario = pedido['codigo_usuario']
    if codigo_usuario in pedidos:
        pedidos[codigo_usuario].append(pedido)
    else:
        pedidos[codigo_usuario] = [pedido]
    
    with open(archivo_pedidos, 'w') as file:
        json.dump(pedidos, file, indent=4)

# TOMAR PEDIDO GUI
def tomar_pedido_gui(codigo_usuario):
    if verificar_usuario(codigo_usuario):
        def submit_pedido():
            equipo = entry_equipo.get()
            talla = var_talla.get().upper()
            if talla not in ['S', 'M', 'L', 'XL']:
                messagebox.showerror("Error", "Talla no válida. Introduce una talla correcta (S, M, L, XL).")
                return
            nombre = entry_nombre.get()
            numero = entry_numero.get() if entry_numero.get().upper() != 'X' else None
            año = entry_año.get()
            equipacion = entry_equipacion.get()
            descripcion = entry_descripcion.get()
            fecha_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

            pedido = {
                'codigo_usuario': codigo_usuario,
                'equipo': equipo,
                'talla': talla,
                'nombre': nombre,
                'numero': numero,
                'año': año,
                'equipacion': equipacion,
                'descripcion': descripcion,
                'fecha': fecha_utc
            }
            
            guardar_pedido(pedido)
            messagebox.showinfo("Éxito", "Pedido realizado con éxito.")
            pedido_window.destroy()

        pedido_window = Toplevel()
        pedido_window.title("Realizar Pedido")

        Label(pedido_window, text="Equipo de la camiseta:").pack()
        entry_equipo = Entry(pedido_window)
        entry_equipo.pack()

        Label(pedido_window, text="Talla de la camiseta (S, M, L, XL):").pack()
        var_talla = StringVar(pedido_window)
        var_talla.set("S")  # default value
        entry_talla = Entry(pedido_window, textvariable=var_talla)
        entry_talla.pack()

        Label(pedido_window, text="Nombre a imprimir en la camiseta:").pack()
        entry_nombre = Entry(pedido_window)
        entry_nombre.pack()

        Label(pedido_window, text="Número a imprimir en la camiseta ('X' si no quiere número):").pack()
        entry_numero = Entry(pedido_window)
        entry_numero.pack()

        Label(pedido_window, text="Año de la camiseta:").pack()
        entry_año = Entry(pedido_window)
        entry_año.pack()

        Label(pedido_window, text="Valor del 1 al 3 para la equipación (1: primera, 2: segunda, 3: tercera):").pack()
        entry_equipacion = Entry(pedido_window)
        entry_equipacion.pack()

        Label(pedido_window, text="Descripción adicional:").pack()
        entry_descripcion = Entry(pedido_window)
        entry_descripcion.pack()

        Button(pedido_window, text="Realizar Pedido", command=submit_pedido).pack()
    else:
        messagebox.showerror("Error", "Usuario no registrado.")

# COMPROBAR PEDIDOS GUI
def comprobar_pedidos_gui(codigo_usuario):
    if not verificar_usuario(codigo_usuario):
        messagebox.showerror("Error", "Usuario no registrado.")
        return
    if os.path.exists(archivo_pedidos):
        with open(archivo_pedidos, 'r') as file:
            pedidos = json.load(file)
        if codigo_usuario in pedidos:
            pedidos_str = ""
            for idx, pedido in enumerate(pedidos[codigo_usuario], 1):
                pedidos_str += f"Pedido {idx}:\n" + "\n".join(f"  {clave}: {valor}" for clave, valor in pedido.items()) + "\n\n"
            messagebox.showinfo("Pedidos", pedidos_str)
        else:
            messagebox.showinfo("Pedidos", "No hay pedidos para este usuario.")
    else:
        messagebox.showinfo("Pedidos", "No hay pedidos registrados.")

# BORRAR PEDIDO GUI
def borrar_pedido_gui(codigo_usuario):
    if not verificar_usuario(codigo_usuario):
        messagebox.showerror("Error", "Usuario no registrado.")
        return
    if os.path.exists(archivo_pedidos):
        with open(archivo_pedidos, 'r') as file:
            pedidos = json.load(file)
        if codigo_usuario in pedidos and pedidos[codigo_usuario]:
            # Mostrar los pedidos y pedir al usuario que elija cuál borrar
            pedidos_str = ""
            for idx, pedido in enumerate(pedidos[codigo_usuario], 1):
                pedidos_str += f"Pedido {idx}:\n" + "\n".join(f"  {clave}: {valor}" for clave, valor in pedido.items()) + "\n\n"
            pedido_num = simpledialog.askinteger("Borrar Pedido", f"Pedidos del usuario:\n\n{pedidos_str}\nIntroduce el número del pedido que deseas borrar:", minvalue=1, maxvalue=len(pedidos[codigo_usuario]))
            
            # Si se proporcionó un número de pedido válido, borrar el pedido
            if pedido_num:
                del pedidos[codigo_usuario][pedido_num - 1]
                with open(archivo_pedidos, 'w') as file:
                    json.dump(pedidos, file, indent=4)
                messagebox.showinfo("Borrar Pedido", "Pedido borrado con éxito.")
            else:
                messagebox.showwarning("Borrar Pedido", "Operación cancelada o número de pedido no válido.")
        else:
            messagebox.showinfo("Borrar Pedido", "No hay pedidos para este usuario.")
    else:
        messagebox.showinfo("Borrar Pedido", "No hay pedidos registrados.")


# VACIAR PEDIDOS GUI
def vaciar_pedidos_gui():
    confirmacion = messagebox.askyesno("Vaciar Pedidos", "¿Estás seguro de que quieres vaciar todos los pedidos?")
    if confirmacion:
        with open(archivo_pedidos, 'w') as file:
            json.dump({}, file, indent=4)
        messagebox.showinfo("Vaciar Pedidos", "Todos los pedidos han sido eliminados.")

# Crear ventana principal
window = tk.Tk()
window.title("Sistema de Pedidos de Camisetas")

# Establecer estilo de la ventana
style = ttk.Style(window)
style.theme_use("clam")

# Crear botones con estilo
btn_realizar_pedido = ttk.Button(window, text="Realizar Pedido", command=lambda: tomar_pedido_gui(simpledialog.askstring("Realizar Pedido", "Introduce tu código único personal:")))
btn_comprobar_pedidos = ttk.Button(window, text="Comprobar Pedidos", command=lambda: comprobar_pedidos_gui(simpledialog.askstring("Comprobar Pedidos", "Introduce tu código único personal:")))
btn_borrar_pedido = ttk.Button(window, text="Borrar Pedido", command=lambda: borrar_pedido_gui(simpledialog.askstring("Borrar Pedido", "Introduce tu código único personal:")))
btn_vaciar_pedidos = ttk.Button(window, text="Vaciar Todos los Pedidos", command=vaciar_pedidos_gui)
btn_salir = ttk.Button(window, text="Salir", command=window.quit)

# Posicionamiento de los botones
btn_realizar_pedido.pack(fill=tk.X, padx=50, pady=5)
btn_comprobar_pedidos.pack(fill=tk.X, padx=50, pady=5)
btn_borrar_pedido.pack(fill=tk.X, padx=50, pady=5)
btn_vaciar_pedidos.pack(fill=tk.X, padx=50, pady=5)
btn_salir.pack(fill=tk.X, padx=50, pady=5)

# Iniciar el bucle principal de la aplicación
window.mainloop()
