import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity
from functions.conexion import ConexionDB
import sqlite3
from tkinter import ttk
from functions.ModuDao import Modulos, listarModulos, consulModulos


class FormModulos():

    def __init__(self, cuerpo_principal, permisos):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Segundo Label con la imagen
        #self.label_imagen = tk.Label(self.barra_inferior, image=bg)
        #self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        #self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_FONDO)
                
        self.marco_modulos = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_modulos.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_modulos, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreatePerm = tk.Button(self.marco_modulos, text="Crear\n Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_Modulo(permisos))
        self.buttonCreatePerm.place(x=140, y=50)

        #self.buttonEditPerm = tk.Button(self.marco_modulos, text="Editar\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
        #                                command=lambda: self.editar_usuario(permisos, self.tablaModulos.item(self.tablaModulos.selection())['values']))
        #self.buttonEditPerm.place(x=250, y=50)
#
        #self.buttonDeletePerm = tk.Button(self.marco_modulos, text="Desactivar\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
        #                                command=lambda: self.desactivarUsuario(permisos))
        #self.buttonDeletePerm.place(x=350, y=50)

        ###################################### Tabla de modulos activos ######################
        where = ""
        if len(where) > 0:
            self.ListaModulos = consulModulos(where)
        else:
            self.ListaModulos = listarModulos()
            self.ListaModulos.reverse()

        self.tablaModulos = ttk.Treeview(self.marco_modulos, column=('nombre','alias','codmod','data_create','data_update'), height=25)
        self.tablaModulos.place(x=145, y=200)

        self.scroll = ttk.Scrollbar(self.marco_modulos, orient='vertical', command=self.tablaModulos.yview)
        self.scroll.place(x=893, y=200, height=526)
        self.tablaModulos.configure(yscrollcommand=self.scroll.set)
        self.tablaModulos.tag_configure('evenrow')

        self.tablaModulos.heading('#0',text="ID")
        self.tablaModulos.heading('#1',text="Nombre")
        self.tablaModulos.heading('#2',text="Alias")
        self.tablaModulos.heading('#3',text="CodMod")
        self.tablaModulos.heading('#4',text="Date-C")
        self.tablaModulos.heading('#5',text="Date-U")


        self.tablaModulos.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaModulos.column("#1", width=60, stretch=False)
        self.tablaModulos.column("#2", width=125, stretch=False)
        self.tablaModulos.column("#3", width=125, stretch=False)
        self.tablaModulos.column("#4", width=125,stretch=False)
        self.tablaModulos.column("#5", width=125, stretch=False)

        
        #self.tablaModulos.bind('<Double-1>', self.crear_usuario)
        for p in self.ListaModulos:
            self.tablaModulos.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))
        
        #self.tablaModulos.bind('<Double-1>', lambda event: self.editar_usuario(event, self.tablaModulos.item(self.tablaModulos.selection())['values']))

    def update_client_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_Modulos.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM Modulos WHERE
                        id LIKE ? OR 
                        coduser LIKE ? OR 
                        username LIKE ? OR 
                        pass LIKE ? OR 
                        idrol LIKE ? OR 
                        date_created LIKE ? OR
                        date_update LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%', 
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.ListaModulos:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaModulos.delete(*self.tablaModulos.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaModulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        self.cursor.close()
        self.connection.close()


    def crear_Modulo(self, permisos):
        #Creacion del top level
        self.topCreateMod = customtkinter.CTkToplevel()
        self.topCreateMod.title("Crear Modulo")
        self.topCreateMod.w = 600
        self.topCreateMod.h = 400
        self.topCreateMod.geometry(f"{self.topCreateMod.w}x{self.topCreateMod.h}")
        self.topCreateMod.resizable(False, False)
        #self.fondo_image = tk.Label(self.topCreateMod)
        #self.fondo_image.place(x=0, y=0, relwidth=1, relheight=1)


        #Centrar la ventana en la pantalla
        screen_width = self.topCreateMod.winfo_screenwidth()
        screen_height = self.topCreateMod.winfo_screenheight()
        x = (screen_width - self.topCreateMod.w) // 2
        y = (screen_height - self.topCreateMod.h) // 2
        self.topCreateMod.geometry(f"+{x}+{y}")

        self.topCreateMod.lift()
        self.topCreateMod.grab_set()
        self.topCreateMod.transient()

        marco_crearpermisos = customtkinter.CTkFrame(self.topCreateMod, width=550,height=350, bg_color="white", fg_color="white")
        marco_crearpermisos.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_crearpermisos, 0.8)

        self.lblinfo = customtkinter.CTkLabel(self.topCreateMod, text="Creacion de nuevo Modulo", font=("Roboto",14))
        self.lblinfo.place(x=205, rely=0.1)
        ############# NOMBRE DEL MODULO
        self.lblnombre = customtkinter.CTkLabel(self.topCreateMod, text='Nombre', font=("Roboto", 14))
        self.lblnombre.place(x=75, y=120)

        self.svnombre_mod = customtkinter.StringVar()
        self.entrynombre_mod = ttk.Entry(self.topCreateMod, style='Modern.TEntry', textvariable=self.svnombre_mod)
        self.entrynombre_mod.place(x=125, y=120)
        self.entrynombre_mod.configure(style='Entry.TEntry')

        ############ NOMBRE DEL ALIAS
        self.lblalias = customtkinter.CTkLabel(self.topCreateMod, text='Alias', font=("Roboto", 14))
        self.lblalias.place(x=75, y=150)

        self.svalias = customtkinter.StringVar()
        self.entryalias = ttk.Entry(self.topCreateMod, style='Modern.TEntry', textvariable=self.svalias)
        self.entryalias.place(x=125, y=150)
        self.entryalias.configure(style='Entry.TEntry')

        ############ CODIGO DEL MODULO
        self.lblcodmod = customtkinter.CTkLabel(self.topCreateMod, text='Codigo \ndel Modulo', font=("Roboto", 14))
        self.lblcodmod.place(x=75, y=180)

        self.svcodmod = customtkinter.StringVar()
        self.entrycodmod = ttk.Entry(self.topCreateMod, style='Modern.TEntry', textvariable=self.svcodmod)
        self.entrycodmod.place(x=125, y=180)
        self.entrycodmod.configure(style='Entry.TEntry')

        