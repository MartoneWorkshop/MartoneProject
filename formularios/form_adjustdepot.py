import tkinter as tk
from config import  COLOR_FONDO
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity
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

        self.fetch_and_display_menus()
        self.buttonCreateGroup = tk.Button(self.marco_adjustdepot, text="Creacion de\nPerfiles", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.add_menu(permisos))
        self.buttonCreateGroup.place(x=225, y=60)

    def add_menu(self, menu, submenu):
        # Insert the menu into the Treeview
        menu_item = self.treeviewDepositos.insert("", "end", text=menu)
        return menu_item
    
    def fetch_and_display_menus(self):
        # Clear the Treeview
        self.treeviewDepositos.delete(*self.treeviewDepositos.get_children())
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM deposito WHERE activo = 1")
        depositos = cursor.fetchall()
        for deposito in depositos:
            deposito_id = deposito[1]
            deposito_name = deposito[2]

            deposito_item = self.treeviewDepositos.insert("", "end", text=deposito_name, tags=("Deposito", deposito_id,))

            cursor.execute("SELECT * FROM grupo WHERE codDep=?",(deposito_id,))
            groups = cursor.fetchall()

            for group in groups:
                group_id = group[2]
                group_name = group[3]
                
                group_item = self.treeviewDepositos.insert(deposito_item, "end", text=group_name, tags=("group", group_id))

                cursor.execute("SELECT * FROM subgrupo WHERE codgrupo=?", (group_id,))
                subgroups = cursor.fetchall()
                for subgroup in subgroups:
                    subgroup_name = subgroup[3]

                    self.treeviewDepositos.insert(group_item, "end", text=subgroup_name, tags=("subgroup", subgroup[0]))
        
        connection.close()
        