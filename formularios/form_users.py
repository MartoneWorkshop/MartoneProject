import tkinter as tk
from config import  COLOR_FONDO
import customtkinter
from util.util_alerts import edit_advice, error_advice, save_advice, set_opacity



class FormUsers():

    def __init__(self, cuerpo_principal, bg, permisos):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Segundo Label con la imagen
        self.label_imagen = tk.Label(self.barra_inferior, image=bg)
        self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_FONDO)
        
        self.marco_create = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_create.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_create, 0.8)

        self.label_accion = customtkinter.CTkLabel(self.marco_create, text="Selector de Acciones para Usuarios", font=("Roboto", 15))
        self.label_accion.place(x=50, y=50)
        self.optionmenu_var = customtkinter.StringVar(value="Accion a Ejecutar")
        self.optionmenu = customtkinter.CTkOptionMenu(self.marco_create,values=["Crear Usuario", "Editar Usuario", "Desactivar Usuario"],
                                         variable=self.optionmenu_var, width=220,height=45, font=("Roboto", 15))
        self.optionmenu.place(x=60, y=100)

        

    