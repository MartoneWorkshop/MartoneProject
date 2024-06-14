import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity
from functions.conexion import ConexionDB
import datetime
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk
from functions.PermDao import Permisos, listarPermisos, consulPermisos, SavePermiso, EditPermiso, PermisoDisable
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


class FormPermisos():

    def __init__(self, cuerpo_principal, permisos):
        self.id = None
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

        self.marco_permisos = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_permisos.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_permisos, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreatePerm = tk.Button(self.marco_permisos, text="Crear\n Permiso", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_permiso(permisos))
        self.buttonCreatePerm.place(x=140, y=50)

        self.buttonEditPerm = tk.Button(self.marco_permisos, text="Editar\n Permiso", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_permiso(permisos, self.tablapermisos.item(self.tablapermisos.selection())['values'])) 
        self.buttonEditPerm.place(x=250, y=50)
        
        self.buttonDeletePerm = tk.Button(self.marco_permisos, text="Desactivar\n Permiso", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.desactivarpermiso(permisos))
        self.buttonDeletePerm.place(x=350, y=50)

        ###################################### Tabla de permisos activos ######################
        where = ""
        if len(where) > 0:
            self.Listapermisos = consulPermisos(where)
        else:
            self.Listapermisos = listarPermisos()
            self.Listapermisos.reverse()

        self.tablapermisos = ttk.Treeview(self.marco_permisos, column=('nombre','alias','codperm','data_create','data_update'), height=25)
        self.tablapermisos.place(x=145, y=200)

        self.scroll = ttk.Scrollbar(self.marco_permisos, orient='vertical', command=self.tablapermisos.yview)
        self.scroll.place(x=893, y=200, height=526)
        self.tablapermisos.configure(yscrollcommand=self.scroll.set)
        self.tablapermisos.tag_configure('evenrow')

        self.tablapermisos.heading('#0',text="ID")
        self.tablapermisos.heading('#1',text="Nombre")
        self.tablapermisos.heading('#2',text="Alias")
        self.tablapermisos.heading('#3',text="Codperm")
        self.tablapermisos.heading('#4',text="Date-C")
        self.tablapermisos.heading('#5',text="Date-U")


        self.tablapermisos.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablapermisos.column("#1", width=60, stretch=False)
        self.tablapermisos.column("#2", width=125, stretch=False)
        self.tablapermisos.column("#3", width=125, stretch=False)
        self.tablapermisos.column("#4", width=125,stretch=False)
        self.tablapermisos.column("#5", width=125, stretch=False)

        
        #self.tablapermisos.bind('<Double-1>', self.crear_usuario)
        for p in self.Listapermisos:
            self.tablapermisos.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))
        
        self.tablapermisos.bind('<Double-1>', lambda event: self.editar_permiso(event, self.tablapermisos.item(self.tablapermisos.selection())['values']))

    def update_client_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_permisos.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM permisos WHERE
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
        for p in self.Listapermisos:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablapermisos.delete(*self.tablapermisos.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablapermisos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        self.cursor.close()
        self.connection.close()


    def crear_permiso(self, permisos):
        #Creacion del top level
        self.topCreatePerm = customtkinter.CTkToplevel()
        self.topCreatePerm.title("Crear permiso")
        self.topCreatePerm.w = 600
        self.topCreatePerm.h = 400
        self.topCreatePerm.geometry(f"{self.topCreatePerm.w}x{self.topCreatePerm.h}")
        self.topCreatePerm.resizable(False, False)
        self.topCreatePerm.configure(bg_color='#6a717e')
        self.topCreatePerm.configure(fg_color='#6a717e')
        

        #Centrar la ventana en la pantalla
        screen_width = self.topCreatePerm.winfo_screenwidth()
        screen_height = self.topCreatePerm.winfo_screenheight()
        x = (screen_width - self.topCreatePerm.w) // 2
        y = (screen_height - self.topCreatePerm.h) // 2
        self.topCreatePerm.geometry(f"+{x}+{y}")

        self.topCreatePerm.lift()
        self.topCreatePerm.grab_set()
        self.topCreatePerm.transient()

        marco_crearpermisos = customtkinter.CTkFrame(self.topCreatePerm, width=550,height=350, bg_color="white", fg_color="white")
        marco_crearpermisos.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_crearpermisos, 0.8)

        self.lblinfo = customtkinter.CTkLabel(self.topCreatePerm, text="Creacion de nuevo permiso", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############# NOMBRE DEL permiso
        self.lblnombre = customtkinter.CTkLabel(self.topCreatePerm, text='Nombre del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblnombre.place(x=102, y=120)

        self.svnombre_perm = customtkinter.StringVar()
        self.entrynombre_perm = ttk.Entry(self.topCreatePerm, style='permern.TEntry', textvariable=self.svnombre_perm)
        self.entrynombre_perm.place(x=95, y=170)
        self.entrynombre_perm.configure(style='Entry.TEntry')

        ############ NOMBRE DEL ALIAS
        self.lblalias = customtkinter.CTkLabel(self.topCreatePerm, text='Alias del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblalias.place(x=255, y=120)

        self.svalias = customtkinter.StringVar()
        self.entryalias = ttk.Entry(self.topCreatePerm, style='permern.TEntry', textvariable=self.svalias, state='disabled')
        self.entryalias.place(x=240, y=170)
        self.entryalias.configure(style='Entry.TEntry')
        self.alias_checkbox_var = tk.IntVar()
        self.alias_checkbox = customtkinter.CTkCheckBox(self.topCreatePerm, text="permificar", bg_color='#e1e3e5', variable=self.alias_checkbox_var, command=self.toggle_alias_entry)
        self.alias_checkbox.place(x=255, y=200)

        ############ CODIGO DEL permiso
        self.lblcodperm = customtkinter.CTkLabel(self.topCreatePerm, text='Codigo del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblcodperm.place(x=392, y=120)

        self.svcodperm = customtkinter.StringVar()
        self.entrycodperm = ttk.Entry(self.topCreatePerm, style='permern.TEntry', textvariable=self.svcodperm, state='disabled')
        self.entrycodperm.place(x=385, y=170)
        self.entrycodperm.configure(style='Entry.TEntry')

        self.svcodperm.set("1000")
        self.entrynombre_perm.bind("<Return>", lambda event: self.Guardarpermiso())
        ######## BOTONE
        self.buttonSaveperm = tk.Button(self.topCreatePerm, text="Crear permiso", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.Guardarpermiso)
        self.buttonSaveperm.place(x=240, y=290)

        def actualizar_alias(*args):
            nombre = self.svnombre_perm.get()
            nombre = nombre.capitalize()  # Capitalizar la primera letra del nombre
            self.svnombre_perm.set(nombre)
            alias = nombre[:4].upper()
            self.svalias.set(alias)

        self.svnombre_perm.trace("w", actualizar_alias)

    def editar_permiso(self, permisos, values):
        self.id = self.tablapermisos.item(self.tablapermisos.selection())['text']
        self.nombredit = self.tablapermisos.item(self.tablapermisos.selection())['values'][0]
        self.aliasedit = self.tablapermisos.item(self.tablapermisos.selection())['values'][1]
        self.codpermedit = self.tablapermisos.item(self.tablapermisos.selection())['values'][2]
        #Creacion del top level
        self.topEditperm = customtkinter.CTkToplevel()
        self.topEditperm.title("Editar permiso")
        self.topEditperm.w = 600
        self.topEditperm.h = 400
        self.topEditperm.geometry(f"{self.topEditperm.w}x{self.topEditperm.h}")
        self.topEditperm.resizable(False, False)
        self.topEditperm.configure(bg_color='#6a717e')
        self.topEditperm.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topEditperm.winfo_screenwidth()
        screen_height = self.topEditperm.winfo_screenheight()
        x = (screen_width - self.topEditperm.w) // 2
        y = (screen_height - self.topEditperm.h) // 2
        self.topEditperm.geometry(f"+{x}+{y}")

        self.topEditperm.lift()
        self.topEditperm.grab_set()
        self.topEditperm.transient()

        marco_editarpermisos = customtkinter.CTkFrame(self.topEditperm, width=550,height=350, bg_color="white", fg_color="white")
        marco_editarpermisos.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_editarpermisos, 0.8)

        self.lblinfo = customtkinter.CTkLabel(self.topEditperm, text="Editar permiso", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############# NOMBRE DEL permiso
        self.lbleditnombre = customtkinter.CTkLabel(self.topEditperm, text='Nombre del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lbleditnombre.place(x=102, y=120)

        self.svnombre_perm = customtkinter.StringVar(value=self.nombredit)
        self.entryeditnombre_perm = ttk.Entry(self.topEditperm, style='permern.TEntry', textvariable=self.svnombre_perm)
        self.entryeditnombre_perm.place(x=95, y=170)
        self.entryeditnombre_perm.configure(style='Entry.TEntry')

        ############ NOMBRE DEL ALIAS
        self.lblalias = customtkinter.CTkLabel(self.topEditperm, text='Alias del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblalias.place(x=255, y=120)

        self.svalias = customtkinter.StringVar(value=self.aliasedit)
        self.entryeditalias = ttk.Entry(self.topEditperm, style='permern.TEntry', textvariable=self.svalias)
        self.entryeditalias.place(x=240, y=170)
        self.entryeditalias.configure(style='Entry.TEntry')

        ############ CODIGO DEL permiso
        self.lbleditcodperm = customtkinter.CTkLabel(self.topEditperm, text='Codigo del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lbleditcodperm.place(x=392, y=120)

        self.svcodperm = customtkinter.StringVar(value=self.codpermedit)
        self.entryeditcodperm = ttk.Entry(self.topEditperm, style='permern.TEntry', textvariable=self.svcodperm)
        self.entryeditcodperm.place(x=385, y=170)
        self.entryeditcodperm.configure(style='Entry.TEntry')

        self.entryeditnombre_perm.bind("<Return>", lambda event: self.Guardarpermiso())
        ######## BOTONE
        self.buttonEditperm = tk.Button(self.topEditperm, text="Actualizar", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.Guardarpermiso)
        self.buttonEditperm.place(x=240, y=290)

        def actualizar_alias(*args):
            nombre = self.svnombre_perm.get()
            nombre = nombre.capitalize()  # Capitalizar la primera letra del nombre
            self.svnombre_perm.set(nombre)
            alias = nombre[:4].upper()
            self.svalias.set(alias)
        self.svnombre_perm.trace("w", actualizar_alias)

    def toggle_alias_entry(self):
        if self.alias_checkbox_var.get() == 1:
            self.entryalias.config(state='normal')
        else:
            self.entryalias.config(state='disabled')

    def Guardarpermiso(self):
        try:
            # Otener el contenido del Entry
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
    
            permisos = permisos(
                self.svnombre_perm.get(),
                self.svalias.get(),
                self.svcodperm.get(),
                date_created,
                date_update
            )
            if self.id is None:
                SavePermiso(permisos)
                self.topCreatePerm.destroy()
            else:
                EditPermiso(permisos, self.id)
                self.topEditperm.destroy()

            self.listarpermisoEnTabla()
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def desactivarpermiso(self, permisos):
        try:
            self.id = self.tablapermisos.item(self.tablapermisos.selection())['text']
            PermisoDisable(self.id)
            self.listarpermisoEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarpermisoEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablapermisos.delete(*self.tablapermisos.get_children())

            if where is not None and len(where) > 0:
                self.Listapermisos = consulPermisos(where)
            else:
                self.Listapermisos = listarPermisos()
                self.Listapermisos.reverse()

            for p in self.Listapermisos:
                self.tablapermisos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarUsuariosEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            