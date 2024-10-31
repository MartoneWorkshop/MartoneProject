import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity, save_advice, edit_advice, error_advice, delete_advice
from functions.conexion import ConexionDB
import datetime
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions.ModuDao import modules, listModules, searchModules, save_module, edit_module, moduleDisable, inactive_modules
from config import WIDTH_LOGO, HEIGHT_LOGO


class FormModules():

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
        ruta_imagen = "imagenes/bg1.jpeg"
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_tk = imagen_tk
        # Crear el Label con la imagen de fondo
        label_fondo = tk.Label(cuerpo_principal, image=imagen_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_fondo = label_fondo
        
        def adjustImage(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
            
        # Configurar el evento <Configure> para redimensionar la imagen de fondo cuando cambie el tamaño de cuerpo_principal
        self.barra_inferior.bind("<Configure>", adjustImage)

        self.marco_modulos = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_modulos.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_modulos, 0.8)
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_modulos = customtkinter.CTkLabel(self.marco_modulos, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_modulos.place(x=220, y=155)

        self.sventrysearch_modulos = customtkinter.StringVar()
        self.entrysearch_modulos = ttk.Entry(self.marco_modulos, textvariable=self.sventrysearch_modulos, style='Modern.TEntry', width=30)
        self.entrysearch_modulos.place(x=270, y=157)
        self.entrysearch_modulos.bind('<KeyRelease>', self.updateSearch)
        if 'CONF1013' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchModStatus = customtkinter.CTkSwitch(self.marco_modulos, variable=self.switchStatus, state='normal',text="Activos", font=("Roboto", 12), command=self.showStatus)
            self.switchModStatus.place(x=700, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchModStatus = customtkinter.CTkSwitch(self.marco_modulos, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.showStatus)
            self.switchModStatus.place(x=700, y=157)

        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateMod = tk.Button(self.marco_modulos, text="Crear\n Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormCreateModule(permisos))
        self.buttonCreateMod.place(x=225, y=60)

        self.buttonEditMod = tk.Button(self.marco_modulos, text="Editar\n Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormEditModule(permisos, self.moduleTable.item(self.moduleTable.selection())['values'])) 
        self.buttonEditMod.place(x=325, y=60)
        
        if 'CONF1010' in permisos:
            self.buttonDeleteMod = tk.Button(self.marco_modulos, text="Desactivar\n Modulo", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateModule(permisos))
            self.buttonDeleteMod.place(x=425, y=60)
        else:
            self.buttonDeleteMod = tk.Button(self.marco_modulos, text="Desactivar\n Modulo", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateModule(permisos))
            self.buttonDeleteMod.place(x=425, y=60)

        ###################################### Tabla de modulos activos ######################
        where = ""
        if len(where) > 0:
            self.listModules = searchModules(where)
        else:
            self.listModules = listModules()
            self.listModules.reverse()

        self.moduleTable = ttk.Treeview(self.marco_modulos, column=('nombre','alias','codmod','data_create','data_update'), height=25)
        self.moduleTable.place(x=210, y=200)

        self.scroll = ttk.Scrollbar(self.marco_modulos, orient='vertical', command=self.moduleTable.yview)
        self.scroll.place(x=832, y=200, height=526)
        self.moduleTable.configure(yscrollcommand=self.scroll.set)
        self.moduleTable.tag_configure('evenrow')

        self.moduleTable.heading('#0',text="ID")
        self.moduleTable.heading('#1',text="Nombre")
        self.moduleTable.heading('#2',text="Alias")
        self.moduleTable.heading('#3',text="CodMod")
        self.moduleTable.heading('#4',text="Date-C")
        self.moduleTable.heading('#5',text="Date-U")


        self.moduleTable.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.moduleTable.column("#1", width=150, stretch=False)
        self.moduleTable.column("#2", width=60, stretch=False)
        self.moduleTable.column("#3", width=100, stretch=False)
        self.moduleTable.column("#4", width=125,stretch=False)
        self.moduleTable.column("#5", width=125, stretch=False)

        
        #self.tablaModulos.bind('<Double-1>', self.crear_usuario)
        for p in self.listModules:
            self.moduleTable.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))
        
        self.moduleTable.bind('<Double-1>', lambda event: self.FormEditModule(event, self.moduleTable.item(self.moduleTable.selection())['values']))
    def showStatus(self):
        if self.switchStatus.get():
            self.switchModStatus.configure(text="Activos")
            self.showActive()
        else:
            self.switchModStatus.configure(text="Inactivos")
            self.showInactive()

    def showActive(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.moduleTable.delete(*self.moduleTable.get_children())
        # Obtener la lista de permisos activos
        activeModule = listModules()
        # Insertar los permisos activos en la tabla
        for p in activeModule:
            self.moduleTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))

    def showInactive(self):
        self.moduleTable.delete(*self.moduleTable.get_children())
        permisos_desactivados = inactive_modules()
        for p in permisos_desactivados:
            self.moduleTable.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))

    def updateSearch(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_modulos.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM modules WHERE
                        id LIKE ? OR 
                        name LIKE ? OR 
                        alias LIKE ? OR 
                        codmod LIKE ? OR 
                        created_at LIKE ? OR
                        updated_at LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.listModules:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.moduleTable.delete(*self.moduleTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.moduleTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()


    def FormCreateModule(self, permisos):
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

        frame_createMod = customtkinter.CTkFrame(self.topCreateMod, width=550,height=350, bg_color="white", fg_color="white")
        frame_createMod.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(frame_createMod, 0.8)

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
        self.entrynombre_mod.bind("<Return>", lambda event: self.SaveModule())
        ######## BOTONE
        self.buttonSaveMod = tk.Button(self.topCreateMod, text="Crear Modulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.SaveModule)
        self.buttonSaveMod.place(x=240, y=290)

        def updateAlias(*args):
            nombre = self.svnombre_mod.get()
            nombre = nombre.capitalize()  # Capitalizar la primera letra del nombre
            self.svnombre_mod.set(nombre)
            alias = nombre[:4].upper()
            self.svalias.set(alias)

        self.svnombre_mod.trace("w", updateAlias)

    def FormEditModule(self, permisos, values):
        if values:
            self.id = self.moduleTable.item(self.moduleTable.selection())['text']
            self.nombredit = self.moduleTable.item(self.moduleTable.selection())['values'][0]
            self.aliasedit = self.moduleTable.item(self.moduleTable.selection())['values'][1]
            self.codmodedit = self.moduleTable.item(self.moduleTable.selection())['values'][2]
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

            frame_editMod = customtkinter.CTkFrame(self.topEditMod, width=550,height=350, bg_color="white", fg_color="white")
            frame_editMod.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(frame_editMod, 0.8)

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

            self.entryeditnombre_mod.bind("<Return>", lambda event: self.SaveModule())
            ######## BOTONE
            self.buttonEditMod = tk.Button(self.topEditMod, text="Actualizar", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.SaveModule)
            self.buttonEditMod.place(x=240, y=290)
        else:
            messagebox.showerror("Error", "Debe seleccionar un modulo")
            
        def updateAlias(*args):
            nombre = self.svnombre_mod.get()
            nombre = nombre.capitalize()  # Capitalizar la primera letra del nombre
            self.svnombre_mod.set(nombre)
            alias = nombre[:4].upper()
            self.svalias.set(alias)
        self.svnombre_mod.trace("w", updateAlias)

    def toggle_alias_entry(self):
        if self.alias_checkbox_var.get() == 1:
            self.entryalias.config(state='normal')
        else:
            self.entryalias.config(state='disabled')

    def SaveModule(self):
        try:
            # Otener el contenido del Entry
            fecha_actual = datetime.datetime.now()
            created_at = fecha_actual.strftime("%Y-%M-%d")
            updated_at = fecha_actual.strftime("%Y-%M-%d %H:%M:%S")
    
            modulos = modules(
                self.svnombre_mod.get(),
                self.svalias.get(),
                self.svcodmod.get(),
                created_at,
                updated_at,
                deleted_at = 'NULL'
            )
            if self.id is None:
                save_module(modulos)
                self.topCreateMod.destroy()
            else:
                edit_module(modulos, self.id)
                self.topEditMod.destroy()

            self.updateTable()
        except Exception as e:
            error_advice()
            mensaje = f'Error en SaveModule, form_modules: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def inactivateModule(self, permisos):
        try:
            self.id = self.moduleTable.item(self.moduleTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este modulo?")
            if confirmar:
                moduleDisable(self.id)
                self.updateTable()
        except Exception as e:
            error_advice()
            mensaje = f'Error en inactivateModule, form_modules: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def updateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.moduleTable.delete(*self.moduleTable.get_children())

            if where is not None and len(where) > 0:
                self.listModules = searchModules(where)
            else:
                self.listModules = listModules()
                self.listModules.reverse()

            for p in self.listModules:
                self.moduleTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en updateTable, form_modules: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            