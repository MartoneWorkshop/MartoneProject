import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity
from functions.conexion import ConexionDB
import datetime
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions.ModuDao import Modulos, listarModulos, consulModulos, SaveModulo, EditModulo, ModuloDisable, ModulosInactivos
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice
from config import WIDTH_LOGO, HEIGHT_LOGO


class FormModulos():

    def __init__(self, cuerpo_principal, permisos):
        self.id = None
        self.idMod = None
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  
        # Segundo Label con la imagen
        ruta_imagen = "imagenes/background.png"
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_tk = imagen_tk
        # Crear el Label con la imagen de fondo
        label_fondo = tk.Label(cuerpo_principal, image=imagen_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_fondo = label_fondo
        
        def ajustar_imagen(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
            
        # Configurar el evento <Configure> para redimensionar la imagen de fondo cuando cambie el tamaño de cuerpo_principal
        self.barra_inferior.bind("<Configure>", ajustar_imagen)

        self.marco_modulos = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_modulos.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_modulos, 0.8)
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_modulos = customtkinter.CTkLabel(self.marco_modulos, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_modulos.place(x=220, y=155)

        self.sventrysearch_modulos = customtkinter.StringVar()
        self.entrysearch_modulos = ttk.Entry(self.marco_modulos, textvariable=self.sventrysearch_modulos, style='Modern.TEntry', width=30)
        self.entrysearch_modulos.place(x=270, y=157)
        self.entrysearch_modulos.bind('<KeyRelease>', self.update_modulos_content)

        self.switchStatus = tk.BooleanVar(value=True)
        self.switchPermStatus = customtkinter.CTkSwitch(self.marco_modulos, variable=self.switchStatus, text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
        self.switchPermStatus.place(x=700, y=157)

        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateMod = tk.Button(self.marco_modulos, text="Crear\n Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_Modulo(permisos))
        self.buttonCreateMod.place(x=225, y=60)

        self.buttonEditMod = tk.Button(self.marco_modulos, text="Editar\n Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_Modulo(permisos, self.tablaModulos.item(self.tablaModulos.selection())['values'])) 
        self.buttonEditMod.place(x=325, y=60)
        
        self.buttonDeleteMod = tk.Button(self.marco_modulos, text="Desactivar\n Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.desactivarModulo(permisos))
        self.buttonDeleteMod.place(x=425, y=60)

        ###################################### Tabla de modulos activos ######################
        where = ""
        if len(where) > 0:
            self.ListaModulos = consulModulos(where)
        else:
            self.ListaModulos = listarModulos()
            self.ListaModulos.reverse()

        self.tablaModulos = ttk.Treeview(self.marco_modulos, column=('nombre','alias','codmod','data_create','data_update'), height=25)
        self.tablaModulos.place(x=210, y=200)

        self.scroll = ttk.Scrollbar(self.marco_modulos, orient='vertical', command=self.tablaModulos.yview)
        self.scroll.place(x=832, y=200, height=526)
        self.tablaModulos.configure(yscrollcommand=self.scroll.set)
        self.tablaModulos.tag_configure('evenrow')

        self.tablaModulos.heading('#0',text="ID")
        self.tablaModulos.heading('#1',text="Nombre")
        self.tablaModulos.heading('#2',text="Alias")
        self.tablaModulos.heading('#3',text="CodMod")
        self.tablaModulos.heading('#4',text="Date-C")
        self.tablaModulos.heading('#5',text="Date-U")


        self.tablaModulos.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaModulos.column("#1", width=150, stretch=False)
        self.tablaModulos.column("#2", width=60, stretch=False)
        self.tablaModulos.column("#3", width=100, stretch=False)
        self.tablaModulos.column("#4", width=125,stretch=False)
        self.tablaModulos.column("#5", width=125, stretch=False)

        
        #self.tablaModulos.bind('<Double-1>', self.crear_usuario)
        for p in self.ListaModulos:
            self.tablaModulos.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))
        
        self.tablaModulos.bind('<Double-1>', lambda event: self.editar_Modulo(event, self.tablaModulos.item(self.tablaModulos.selection())['values']))
    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.mostrarModulosActivos()
        else:
            self.mostrarModulosDesactivados()

    def mostrarModulosActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaModulos.delete(*self.tablaModulos.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listarModulos()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaModulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))

    def mostrarModulosDesactivados(self):
        self.tablaModulos.delete(*self.tablaModulos.get_children())
        permisos_desactivados = ModulosInactivos()
        for p in permisos_desactivados:
            self.tablaModulos.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))

    def update_modulos_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_modulos.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM modulos WHERE
                        id LIKE ? OR 
                        name LIKE ? OR 
                        alias LIKE ? OR 
                        codmod LIKE ? OR 
                        date_created LIKE ? OR
                        date_update LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.ListaModulos:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaModulos.delete(*self.tablaModulos.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaModulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()


    def crear_Modulo(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateMod = customtkinter.CTkToplevel()
        self.topCreateMod.title("Crear Modulo")
        self.topCreateMod.w = 600
        self.topCreateMod.h = 400
        self.topCreateMod.geometry(f"{self.topCreateMod.w}x{self.topCreateMod.h}")
        self.topCreateMod.resizable(False, False)
        self.topCreateMod.configure(bg_color='#6a717e')
        self.topCreateMod.configure(fg_color='#6a717e')
        

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

        self.lblinfo = customtkinter.CTkLabel(self.topCreateMod, text="Creacion de nuevo Modulo", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############# NOMBRE DEL MODULO
        self.lblnombre = customtkinter.CTkLabel(self.topCreateMod, text='Nombre del Modulo', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblnombre.place(x=102, y=120)

        self.svnombre_mod = customtkinter.StringVar()
        self.entrynombre_mod = ttk.Entry(self.topCreateMod, style='Modern.TEntry', textvariable=self.svnombre_mod)
        self.entrynombre_mod.place(x=95, y=170)
        self.entrynombre_mod.configure(style='Entry.TEntry')

        ############ NOMBRE DEL ALIAS
        self.lblalias = customtkinter.CTkLabel(self.topCreateMod, text='Alias del Modulo', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblalias.place(x=255, y=120)

        self.svalias = customtkinter.StringVar()
        self.entryalias = ttk.Entry(self.topCreateMod, style='Modern.TEntry', textvariable=self.svalias, state='disabled')
        self.entryalias.place(x=240, y=170)
        self.entryalias.configure(style='Entry.TEntry')
        self.alias_checkbox_var = tk.IntVar()
        self.alias_checkbox = customtkinter.CTkCheckBox(self.topCreateMod, text="Modificar", bg_color='#e1e3e5', variable=self.alias_checkbox_var, command=self.toggle_alias_entry)
        self.alias_checkbox.place(x=255, y=200)

        ############ CODIGO DEL MODULO
        self.lblcodmod = customtkinter.CTkLabel(self.topCreateMod, text='Codigo del Modulo', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblcodmod.place(x=392, y=120)

        self.svcodmod = customtkinter.StringVar()
        self.entrycodmod = ttk.Entry(self.topCreateMod, style='Modern.TEntry', textvariable=self.svcodmod, state='disabled')
        self.entrycodmod.place(x=385, y=170)
        self.entrycodmod.configure(style='Entry.TEntry')

        self.svcodmod.set("1000")
        self.entrynombre_mod.bind("<Return>", lambda event: self.GuardarModulo())
        ######## BOTONE
        self.buttonSaveMod = tk.Button(self.topCreateMod, text="Crear Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarModulo)
        self.buttonSaveMod.place(x=240, y=290)

        def actualizar_alias(*args):
            nombre = self.svnombre_mod.get()
            nombre = nombre.capitalize()  # Capitalizar la primera letra del nombre
            self.svnombre_mod.set(nombre)
            alias = nombre[:4].upper()
            self.svalias.set(alias)

        self.svnombre_mod.trace("w", actualizar_alias)

    def editar_Modulo(self, permisos, values):
        self.id = self.tablaModulos.item(self.tablaModulos.selection())['text']
        self.nombredit = self.tablaModulos.item(self.tablaModulos.selection())['values'][0]
        self.aliasedit = self.tablaModulos.item(self.tablaModulos.selection())['values'][1]
        self.codmodedit = self.tablaModulos.item(self.tablaModulos.selection())['values'][2]
        #Creacion del top level
        self.topEditMod = customtkinter.CTkToplevel()
        self.topEditMod.title("Editar Modulo")
        self.topEditMod.w = 600
        self.topEditMod.h = 400
        self.topEditMod.geometry(f"{self.topEditMod.w}x{self.topEditMod.h}")
        self.topEditMod.resizable(False, False)
        self.topEditMod.configure(bg_color='#6a717e')
        self.topEditMod.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topEditMod.winfo_screenwidth()
        screen_height = self.topEditMod.winfo_screenheight()
        x = (screen_width - self.topEditMod.w) // 2
        y = (screen_height - self.topEditMod.h) // 2
        self.topEditMod.geometry(f"+{x}+{y}")

        self.topEditMod.lift()
        self.topEditMod.grab_set()
        self.topEditMod.transient()

        marco_editarpermisos = customtkinter.CTkFrame(self.topEditMod, width=550,height=350, bg_color="white", fg_color="white")
        marco_editarpermisos.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_editarpermisos, 0.8)

        self.lblinfo = customtkinter.CTkLabel(self.topEditMod, text="Editar Modulo", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############# NOMBRE DEL MODULO
        self.lbleditnombre = customtkinter.CTkLabel(self.topEditMod, text='Nombre del Modulo', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lbleditnombre.place(x=102, y=120)

        self.svnombre_mod = customtkinter.StringVar(value=self.nombredit)
        self.entryeditnombre_mod = ttk.Entry(self.topEditMod, style='Modern.TEntry', textvariable=self.svnombre_mod)
        self.entryeditnombre_mod.place(x=95, y=170)
        self.entryeditnombre_mod.configure(style='Entry.TEntry')

        ############ NOMBRE DEL ALIAS
        self.lblalias = customtkinter.CTkLabel(self.topEditMod, text='Alias del Modulo', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblalias.place(x=255, y=120)

        self.svalias = customtkinter.StringVar(value=self.aliasedit)
        self.entryeditalias = ttk.Entry(self.topEditMod, style='Modern.TEntry', textvariable=self.svalias)
        self.entryeditalias.place(x=240, y=170)
        self.entryeditalias.configure(style='Entry.TEntry')

        ############ CODIGO DEL MODULO
        self.lbleditcodmod = customtkinter.CTkLabel(self.topEditMod, text='Codigo del Modulo', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lbleditcodmod.place(x=392, y=120)

        self.svcodmod = customtkinter.StringVar(value=self.codmodedit)
        self.entryeditcodmod = ttk.Entry(self.topEditMod, style='Modern.TEntry', textvariable=self.svcodmod)
        self.entryeditcodmod.place(x=385, y=170)
        self.entryeditcodmod.configure(style='Entry.TEntry')

        self.entryeditnombre_mod.bind("<Return>", lambda event: self.GuardarModulo())
        ######## BOTONE
        self.buttonEditMod = tk.Button(self.topEditMod, text="Actualizar", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarModulo)
        self.buttonEditMod.place(x=240, y=290)

        def actualizar_alias(*args):
            nombre = self.svnombre_mod.get()
            nombre = nombre.capitalize()  # Capitalizar la primera letra del nombre
            self.svnombre_mod.set(nombre)
            alias = nombre[:4].upper()
            self.svalias.set(alias)
        self.svnombre_mod.trace("w", actualizar_alias)

    def toggle_alias_entry(self):
        if self.alias_checkbox_var.get() == 1:
            self.entryalias.config(state='normal')
        else:
            self.entryalias.config(state='disabled')

    def GuardarModulo(self):
        try:
            # Otener el contenido del Entry
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
    
            modulos = Modulos(
                self.svnombre_mod.get(),
                self.svalias.get(),
                self.svcodmod.get(),
                date_created,
                date_update
            )
            if self.id is None:
                SaveModulo(modulos)
                self.topCreateMod.destroy()
            else:
                EditModulo(modulos, self.id)
                self.topEditMod.destroy()

            self.listarModuloEnTabla()
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def desactivarModulo(self, permisos):
        try:
            self.id = self.tablaModulos.item(self.tablaModulos.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este modulo?")
            if confirmar:
                ModuloDisable(self.id)
                self.listarModuloEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarModuloEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaModulos.delete(*self.tablaModulos.get_children())

            if where is not None and len(where) > 0:
                self.ListaModulos = consulModulos(where)
            else:
                self.ListaModulos = listarModulos()
                self.ListaModulos.reverse()

            for p in self.ListaModulos:
                self.tablaModulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarModulosEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            