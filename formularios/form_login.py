import tkinter as tk
import customtkinter
from config import  COLOR_FONDO
from functions.conexion import ConexionDB
from tkinter import ttk, messagebox, Tk, Label, Canvas, PhotoImage
from PIL import ImageTk, Image, ImageFilter





class FormLogin():
    def __init__(self, cuerpo_principal):
        self.cuerpo_principal = cuerpo_principal
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

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

            else:
                title = 'Log In Fail'
                mensaje = 'Datos validados incorrectamente.'
                messagebox.showerror(title, mensaje)

        marco_login = customtkinter.CTkFrame(cuerpo_principal, fg_color="#F1EFED", width=1120, height=600)
        marco_login.place(relx=0.5, rely=0.5, anchor="center")
        #LOGIN USER
        lbluser = Label(marco_login, text="Usuario: ")
        lbluser.pack(pady=1, padx=6)
        lbluser.place(x=450, y=154)

        sv_datauser = customtkinter.StringVar()
        entryuser = customtkinter.CTkEntry(marco_login, textvariable=sv_datauser, width=100)
        entryuser.place(x=525, y=150)

        #LOGIN PASSWORD
        lblpass = Label(marco_login, text="Contraseña: ")
        lblpass.pack(pady=1, padx=6)
        lblpass.place(x=450, y=194)

        sv_datapass = customtkinter.StringVar()
        entrypass = customtkinter.CTkEntry(marco_login, textvariable=sv_datapass, show="*", width=100)
        entrypass.place(x=525, y=190)
        entrypass.bind("<Return>", lambda event: validarDatos())
        
        #LOGIN BOTON
        btnLogIn = customtkinter.CTkButton(marco_login, text="Ingresar", width=60, command=validarDatos)
        btnLogIn.pack(pady=12, padx=5)
        btnLogIn.place(x=500, y=235)
