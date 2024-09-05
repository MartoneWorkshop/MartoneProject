import customtkinter
import ctypes
import tempfile
import os
from tkinter import ttk, messagebox, Tk, Label, Canvas, PhotoImage
from formularios.form_maestro import FormularioMaestroDesign
import time
from PIL import ImageTk, Image, ImageFilter
from functions.conexion import ConexionDB

root = customtkinter.CTk()
root.geometry("300x340")
root.resizable(False, False)
root.title("Log in")
root.iconbitmap("imagenes/logo_ico.ico")

# Establecer el icono en la barra de herramientas
icon_path = "imagenes/logo_ico.ico"
ctypes.windll.kernel32.SetConsoleIcon(ctypes.windll.shell32.Shell_GetCachedImageIndexW(icon_path, 0, 0))

imagen = Image.open("imagenes/login_bg.png")
imagen_resized = imagen.resize((root.winfo_width(), root.winfo_height()))
nueva_dimension = (301, 341)
imagen_ajustada = imagen.resize(nueva_dimension)
imagen_tk = ImageTk.PhotoImage(imagen_ajustada)
#
label_fondo = Label(root, image=imagen_tk, text="")
label_fondo.place(x=-2, y=-2)


def main():
    print("TEST")

def validarDatos():
    conexion = ConexionDB()
    username = sv_datauser.get()
    password = sv_datapass.get()

    sql = f"SELECT pass FROM usuarios WHERE username = '{username}' AND pass = '{password}'"
    conexion.ejecutar_consulta(sql)
    resultado = conexion.obtener_resultado()

    if resultado:
        title = 'Log In Success'
        mensaje = 'Datos validados correctamente.'
        messagebox.showinfo(title, mensaje)
        ocultar()
        open_program()
        
    else:
        title = 'Log In Fail'
        mensaje = 'Datos validados incorrectamente.'
        messagebox.showerror(title, mensaje)

color_dominante = imagen_ajustada.getpixel((60, 140))
color_hex = '#{:02x}{:02x}{:02x}'.format(*color_dominante)


#LOGIN USER
lbluser = Label(root, text="Usuario: ")
lbluser.configure(bg=color_hex)
lbluser.pack(pady=1, padx=6)
lbluser.place(x=50, y=142)


sv_datauser = customtkinter.StringVar()
entryuser = customtkinter.CTkEntry(root, textvariable=sv_datauser, width=100)
entryuser.place(x=120, y=140)
entryuser.configure(bg_color=color_hex)


#LOGIN PASSWORD
lblpass = Label(root, text="Contraseña: ")
lblpass.configure(bg=color_hex)
lblpass.pack(pady=1, padx=6)
lblpass.place(x=50, y=180)


sv_datapass = customtkinter.StringVar()
entrypass = customtkinter.CTkEntry(root, textvariable=sv_datapass, show="*", width=100)
entrypass.place(x=120, y=180)
entrypass.bind("<Return>", lambda event: validarDatos())
entrypass.configure(bg_color=color_hex)



btnLogIn = customtkinter.CTkButton(root, text="Ingresar", width=60, command=validarDatos)
btnLogIn.configure(bg_color=color_hex)
btnLogIn.pack(pady=12, padx=5)
btnLogIn.place(x=130, y=220)

def ocultar():
    root.withdraw()

def cerrar_app():
    root.quit()

def open_program():
    toplevel = customtkinter.CTkToplevel()
    toplevel.title("Policlinica de Especialidades - Gestion de Inventario")
    toplevel.geometry("1440x900")
    app = FormularioMaestroDesign()
    app.mainloop()
    
    #open_frame = FormularioMaestroDesign(toplevel)
    #open_frame.pack()
#
    app.protocol("WM_DELETE_WINDOW", cerrar_app)

root.mainloop()