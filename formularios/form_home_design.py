import tkinter as tk
from config import  COLOR_FONDO



class FormularioHomeDesign():

    def __init__(self, cuerpo_principal, bg):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(
        self.barra_superior, text="SECCION HOME")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_FONDO)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Segundo Label con la imagen
        self.label_imagen = tk.Label(self.barra_inferior, image=bg)
        self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_FONDO)
        
        
        
