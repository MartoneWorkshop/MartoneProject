import tkinter as tk
from config import  COLOR_FONDO
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity
from functions.AdjustDepotsDao import Deposito, Grupo, SubGrupo, obtener_depositos, obtener_grupos, obtener_subgrupos
from config import COLOR_MENU_LATERAL
import sqlite3


class FormAdjustDepot():

    def __init__(self, cuerpo_principal, permisos):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        ruta_imagen = "imagenes/background.png"
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_tk = imagen_tk
        # Crear el Label con la imagen de fondo
        label_fondo = tk.Label(cuerpo_principal, image=imagen_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_fondo = label_fondo
        # Configurar el Label para que se ajuste automáticamente al tamaño del frame
        def ajustar_imagen(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
        
        self.barra_inferior.bind("<Configure>", ajustar_imagen)

        # Segundo Label con la imagen
        self.label_imagen = tk.Label(self.barra_inferior, image=imagen_tk)
        self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_FONDO)

        self.marco_adjustdepot = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_adjustdepot.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_adjustdepot, 0.8)
        

        self.treeviewDepositos= ttk.Treeview(self.marco_adjustdepot, height=36)
        self.treeviewDepositos.place(x=25, y=30)

        self.listar_dgs()
        self.buttonCreateGroup = tk.Button(self.marco_adjustdepot, text="Crear Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_deposito(permisos))
        self.buttonCreateGroup.place(x=235, y=60)

    def crear_deposito(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateDepot = customtkinter.CTkToplevel()
        self.topCreateDepot.title("Crear Modulo")
        self.topCreateDepot.w = 600
        self.topCreateDepot.h = 400
        self.topCreateDepot.geometry(f"{self.topCreateDepot.w}x{self.topCreateDepot.h}")
        self.topCreateDepot.resizable(False, False)
        self.topCreateDepot.configure(bg_color='#6a717e')
        self.topCreateDepot.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topCreateDepot.winfo_screenwidth()
        screen_height = self.topCreateDepot.winfo_screenheight()
        x = (screen_width - self.topCreateDepot.w) // 2
        y = (screen_height - self.topCreateDepot.h) // 2
        self.topCreateDepot.geometry(f"+{x}+{y}")

        self.topCreateDepot.lift()
        self.topCreateDepot.grab_set()
        self.topCreateDepot.transient()

        marco_createDepot = customtkinter.CTkFrame(self.topCreateDepot, width=550,height=350, bg_color="white", fg_color="white")
        marco_createDepot.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_createDepot, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_createDepot, text="Creacion de un nuevo Deposito", font=("Roboto",14))
        self.lblinfo.place(x=187, rely=0.1)

        



    
    def listar_dgs(self):
        self.treeviewDepositos.delete(*self.treeviewDepositos.get_children())
        depositos = obtener_depositos()
    
        for deposito in depositos:
            deposito_id = deposito[1]
            deposito_name = deposito[2]

            deposito_item = self.treeviewDepositos.insert("", "end", text=deposito_name, tags=("Deposito", deposito_id))

            groups = obtener_grupos(deposito_id)

            for group in groups:
                group_id = group[2]
                group_name = group[3]

                group_item = self.treeviewDepositos.insert(deposito_item, "end", text=group_name, tags=("group", group_id))

                subgroups = obtener_subgrupos(group_id)

                for subgroup in subgroups:
                    subgroup_name = subgroup[3]

                    self.treeviewDepositos.insert(group_item, "end", text=subgroup_name, tags=("subgroup", subgroup[0]))