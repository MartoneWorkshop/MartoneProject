import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity
import traceback
from functions.conexion import ConexionDB
import datetime
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk
from functions.ProfileDao import Roles, listarPerfil, consulPerfiles, SaveProfile, EditProfile, ProfileDisable, ActualizacionPermisos, PerfilesInactivos,GuardarNuevosPermisos, LimpiarPermisos
from util.util_functions import obtener_permisos, ObtenerListaDeModulos, ObtenerPermisosDeModulos, ObtenerRoles, ObtenerModulos, ObtenerPermisosAsignados
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice
from config import WIDTH_LOGO, HEIGHT_LOGO


class FormPerfiles():

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

        self.marco_perfiles = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_perfiles.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_perfiles, 0.8)
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_perfiles = customtkinter.CTkLabel(self.marco_perfiles, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_perfiles.place(x=220, y=155)

        self.sventrysearch_perfiles = customtkinter.StringVar()
        self.entrysearch_perfiles = ttk.Entry(self.marco_perfiles, textvariable=self.sventrysearch_perfiles, style='Modern.TEntry', width=30)
        self.entrysearch_perfiles.place(x=270, y=157)
        self.entrysearch_perfiles.bind('<KeyRelease>', self.update_profiles_content)

        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateProfile = tk.Button(self.marco_perfiles, text="Creacion de\nPerfiles", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_Perfiles(permisos))
        self.buttonCreateProfile.place(x=225, y=60)

        self.buttonEditProfile = tk.Button(self.marco_perfiles, text="Edicion de\nPerfil", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_Perfil(permisos, self.tablaPerfiles.item(self.tablaPerfiles.selection())['values'])) 
        self.buttonEditProfile.place(x=355, y=60)

        if 'CONF1007' in permisos:
            self.buttonDeleteProfile = tk.Button(self.marco_perfiles, text="Desactivar\n Perfil", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarPerfil(permisos))
            self.buttonDeleteProfile.place(x=475, y=60)
        else:
            self.buttonDeleteProfile = tk.Button(self.marco_perfiles, text="Desactivar\n Perfil", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarPerfil(permisos))
            self.buttonDeleteProfile.place(x=475, y=60)

        if 'CONF1008' in permisos:
            self.buttonModPerm = tk.Button(self.marco_perfiles, text="Modificar\n Permisos", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.modificarPermisos(permisos, self.tablaPerfiles.item(self.tablaPerfiles.selection())['values']))
            self.buttonModPerm.place(x=600, y=60)
        else:
            self.buttonModPerm = tk.Button(self.marco_perfiles, text="Modificar\n Permisos", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.modificarPermisos(permisos, self.tablaPerfiles.item(self.tablaPerfiles.selection())['values']))
            self.buttonModPerm.place(x=600, y=60)

        if 'CONF1012' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchPermStatus = customtkinter.CTkSwitch(self.marco_perfiles, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchPermStatus.place(x=700, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchPermStatus = customtkinter.CTkSwitch(self.marco_perfiles, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchPermStatus.place(x=700, y=157)

        ###################################### Tabla de modulos activos ######################
        where = ""
        if len(where) > 0:
            self.ListaPerfiles = consulPerfiles(where)
        else:
            self.ListaPerfiles = listarPerfil()
            self.ListaPerfiles.reverse()

        self.tablaPerfiles = ttk.Treeview(self.marco_perfiles, column=('Nombre','Data_create','Data_update'), height=25)
        self.tablaPerfiles.place(x=210, y=200)

        self.scroll = ttk.Scrollbar(self.marco_perfiles, orient='vertical', command=self.tablaPerfiles.yview)
        self.scroll.place(x=832, y=200, height=526)
        self.tablaPerfiles.configure(yscrollcommand=self.scroll.set)
        self.tablaPerfiles.tag_configure('evenrow')

        self.tablaPerfiles.heading('#0',text="ID")
        self.tablaPerfiles.heading('#1',text="Nombre")
        self.tablaPerfiles.heading('#2',text="Date-C")
        self.tablaPerfiles.heading('#3',text="Date-U")

        self.tablaPerfiles.column("#0", width=100, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaPerfiles.column("#1", width=170, stretch=False)
        self.tablaPerfiles.column("#2", width=175, stretch=False)
        self.tablaPerfiles.column("#3", width=175, stretch=False)

        
        #self.tablaPerfiles.bind('<Double-1>', self.crear_usuario)
        for p in self.ListaPerfiles:
            self.tablaPerfiles.insert('',0,text=p[0], values=(p[1],p[2],p[3]))
        
        
        self.tablaPerfiles.bind('<Double-1>', lambda event: self.editar_Perfil(event, self.tablaPerfiles.item(self.tablaPerfiles.selection())['values']))
    
    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchPermStatus.configure(text="Activos")
            self.mostrarPerfilActivos()
        else:
            self.switchPermStatus.configure(text="Inactivos")
            self.mostrarPerfilDesactivados()

    def mostrarPerfilActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaPerfiles.delete(*self.tablaPerfiles.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listarPerfil()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaPerfiles.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))

    def mostrarPerfilDesactivados(self):
        self.tablaPerfiles.delete(*self.tablaPerfiles.get_children())
        permisos_desactivados = PerfilesInactivos()
        for p in permisos_desactivados:
            self.tablaPerfiles.insert('',0, text=p[0], values=(p[1],p[2],p[3]))

    def update_profiles_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_perfiles.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM roles WHERE
                        id LIKE ? OR 
                        name LIKE ? OR 
                        date_created LIKE ? OR
                        date_update LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.ListaPerfiles:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaPerfiles.delete(*self.tablaPerfiles.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaPerfiles.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
        self.cursor.close()
        self.connection.close()


    def crear_Perfiles(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateProfile = customtkinter.CTkToplevel()
        self.topCreateProfile.title("Crear Modulo")
        self.topCreateProfile.w = 600
        self.topCreateProfile.h = 400
        self.topCreateProfile.geometry(f"{self.topCreateProfile.w}x{self.topCreateProfile.h}")
        self.topCreateProfile.resizable(False, False)
        self.topCreateProfile.configure(bg_color='#6a717e')
        self.topCreateProfile.configure(fg_color='#6a717e')
        

        #Centrar la ventana en la pantalla
        screen_width = self.topCreateProfile.winfo_screenwidth()
        screen_height = self.topCreateProfile.winfo_screenheight()
        x = (screen_width - self.topCreateProfile.w) // 2
        y = (screen_height - self.topCreateProfile.h) // 2
        self.topCreateProfile.geometry(f"+{x}+{y}")

        self.topCreateProfile.lift()
        self.topCreateProfile.grab_set()
        self.topCreateProfile.transient()

        marco_createProfile = customtkinter.CTkFrame(self.topCreateProfile, width=550,height=350, bg_color="white", fg_color="white")
        marco_createProfile.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_createProfile, 0.8)

        self.lblinfo = customtkinter.CTkLabel(self.topCreateProfile, text="Creacion de un nuevo Perfil", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############# NOMBRE DEL MODULO
        self.lblnombre = customtkinter.CTkLabel(self.topCreateProfile, text='Nombre del Perfil', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblnombre.place(x=102, y=120)

        self.svnombre_perfil = customtkinter.StringVar()
        self.entrynombre_perfil = ttk.Entry(self.topCreateProfile, style='Modern.TEntry', textvariable=self.svnombre_perfil)
        self.entrynombre_perfil.place(x=95, y=170)
        self.entrynombre_perfil.configure(style='Entry.TEntry')

    
        self.entrynombre_perfil.bind("<Return>", lambda event: self.GuardarPerfiles())
        ######## BOTONE
        self.buttonSaveProfile = tk.Button(self.topCreateProfile, text="Crear Perfil", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarPerfiles)
        self.buttonSaveProfile.place(x=240, y=290)


    def editar_Perfil(self, permisos, values):
        if values:
            self.id = self.tablaPerfiles.item(self.tablaPerfiles.selection())['text']
            self.nombredit = self.tablaPerfiles.item(self.tablaPerfiles.selection())['values'][0]
            #Creacion del top level
            self.topEditProfile = customtkinter.CTkToplevel()
            self.topEditProfile.title("Editar Perfil")
            self.topEditProfile.w = 600
            self.topEditProfile.h = 400
            self.topEditProfile.geometry(f"{self.topEditProfile.w}x{self.topEditProfile.h}")
            self.topEditProfile.resizable(False, False)
            self.topEditProfile.configure(bg_color='#6a717e')
            self.topEditProfile.configure(fg_color='#6a717e')

            #Centrar la ventana en la pantalla
            screen_width = self.topEditProfile.winfo_screenwidth()
            screen_height = self.topEditProfile.winfo_screenheight()
            x = (screen_width - self.topEditProfile.w) // 2
            y = (screen_height - self.topEditProfile.h) // 2
            self.topEditProfile.geometry(f"+{x}+{y}")

            self.topEditProfile.lift()
            self.topEditProfile.grab_set()
            self.topEditProfile.transient()

            marco_editarpermisos = customtkinter.CTkFrame(self.topEditProfile, width=550,height=350, bg_color="white", fg_color="white")
            marco_editarpermisos.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(marco_editarpermisos, 0.8)

            self.lblinfo = customtkinter.CTkLabel(self.topEditProfile, text="Editar Perfil", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
            self.lblinfo.place(relx=0.43, rely=0.1)

            ############# NOMBRE DEL MODULO
            self.lbleditnombre = customtkinter.CTkLabel(self.topEditProfile, text='Nombre del Perfil', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
            self.lbleditnombre.place(relx=0.42, y=120)

            self.svnombre_perfil = customtkinter.StringVar(value=self.nombredit)
            self.entryeditnombre_perfil = ttk.Entry(self.topEditProfile, style='Modern.TEntry', textvariable=self.svnombre_perfil)
            self.entryeditnombre_perfil.place(relx=0.4, y=170)
            self.entryeditnombre_perfil.configure(style='Entry.TEntry')

            self.entryeditnombre_perfil.bind("<Return>", lambda event: self.GuardarPerfiles())
            ######## BOTONE
            self.buttonEditProfile = tk.Button(self.topEditProfile, text="Actualizar", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarPerfiles)
            self.buttonEditProfile.place(x=250, y=290)
        else:
            messagebox.showerror("Error", "Debe seleccionar un perfil")


    def modificarPermisos(self, permisos, values):
        #Creacion del top level
        self.topModperm = customtkinter.CTkToplevel()
        self.topModperm.title("Modificar Permisos a Usuario")
        self.topModperm.w = 800
        self.topModperm.h = 600
        self.topModperm.geometry(f"{self.topModperm.w}x{self.topModperm.h}")
        self.topModperm.resizable(False, False)
        self.topModperm.configure(bg_color='#6a717e')
        self.topModperm.configure(fg_color='#6a717e')
        #Centrar la ventana en la pantalla
        screen_width = self.topModperm.winfo_screenwidth()
        screen_height = self.topModperm.winfo_screenheight()
        x = (screen_width - self.topModperm.w) // 2
        y = (screen_height - self.topModperm.h) // 2
        self.topModperm.geometry(f"+{x}+{y}")
        self.topModperm.lift()
        self.topModperm.grab_set()
        self.topModperm.transient()
        #Datos para el usuario
        marco_modperm = customtkinter.CTkFrame(self.topModperm, width=700,height=500, bg_color="white", fg_color="white")
        marco_modperm.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(marco_modperm, 0.8)
        self.tab_permisos = customtkinter.CTkTabview(marco_modperm, width=620,height=430)
        self.tab_permisos.place(x=40, y=30)
        perfil_id = self.tablaPerfiles.item(self.tablaPerfiles.selection())['text'] 
        modulos = ObtenerListaDeModulos()
        asigperm = ObtenerPermisosAsignados(perfil_id)
        self.tabs = {}
        interruptores = {}
        for modulo in modulos:
            nombre_modulo = modulo['name']
            tab = self.tab_permisos.add(nombre_modulo)
            self.tabs[nombre_modulo] = tab
            if modulo == 'Home':
                self.tab_permisos.set(tab)
            id_modulo = modulo['id']
            permisos_modulo = ObtenerPermisosDeModulos(id_modulo)
            if permisos_modulo:
                x_offset = 0.1
                y_offset = 0.1
                fila_actual = 0
                columna_actual = 0
                max_filas = 8
                max_columnas = 3
                for permiso in permisos_modulo:
                    nombre_permiso = permiso['name']
                    permisos_modulos = [permiso['codperm']]
                    asigperm_active = [permiso['codpermiso'] for permiso in asigperm]
                    if any(permiso_modulo in asigperm_active for permiso_modulo in permisos_modulos):
                        switch_var_permiso = tk.BooleanVar(value=True)
                    else:
                        switch_var_permiso = tk.BooleanVar(value=False)
                    switch_permiso = customtkinter.CTkSwitch(tab, variable=switch_var_permiso, text=nombre_permiso)
                    interruptores[switch_permiso] = permiso
                # Clcular posición relativa en la cuadrícula
                    relx = x_offset + (columna_actual * 0.30)
                    rely = y_offset + (fila_actual * 0.10)
                    switch_permiso.place(relx=relx, rely=rely)
                    columna_actual += 1
                    if columna_actual >= max_columnas:
                        columna_actual = 0
                        fila_actual += 1
                        if fila_actual >= max_filas:
                            # Se alcanzó el límite de filas, salir del bucle
                            break
        self.buttonActualizar = tk.Button(self.topModperm, text="Actualizar Permisos", font=("Roboto", 12), 
                                        bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, 
                                        padx=10, command=lambda: self.ActualizarPermisos(perfil_id, interruptores))
        self.buttonActualizar.place(x=323, y=515)

    def guardarPermisosSeleccionados(self, interruptores):
        try:
            permisos_seleccionados = [permiso['codperm'] for interruptor, permiso in interruptores.items() if permiso.get('codperm') and interruptor.get()]
            return permisos_seleccionados
    
        except Exception as e:
            error_advice()
            mensaje = f'Error en guardarPermisosSeleccionados, form_Perfiles: {str(e)}'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    
    def ActualizarPermisos(self, perfil_id, interruptores):
        try:
            permisos_seleccionados = self.guardarPermisosSeleccionados(interruptores)
            LimpiarPermisos(perfil_id)
            
            GuardarNuevosPermisos(perfil_id, permisos_seleccionados)
            #permisos_seleccionados = guardarPermisosSeleccionados()
            #GuardarNuevosPermisos(perfil_id, permisos_seleccionados)
            self.topModperm.destroy()
        except Exception as e:
            error_advice()
            mensaje = f'Error en ActualizarPermisos, form_Perfiles: {str(e)}'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    
    def GuardarPerfiles(self):
        try:
            # Otener el contenido del Entry
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%Y %H:%M:%S")
    
            roles = Roles(
                self.svnombre_perfil.get(),
                date_created,
                date_update
            )
            if self.id is None:
                SaveProfile(roles)
                self.topCreateProfile.destroy()
            else:
                EditProfile(roles, self.id)
                self.topEditProfile.destroy()
            self.listarPerfilEnTabla()

        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarPerfiles, form_Perfiles: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def desactivarPerfil(self, permisos):
        try:
            self.id = self.tablaPerfiles.item(self.tablaPerfiles.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este perfil?")
            if confirmar and 'CONF1007' in permisos:
                ProfileDisable(self.id)
                self.listarPerfilEnTabla()
            else:
                messagebox.showerror("Error", "No posee permisos suficientes para realizar esta accion.")
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarUsuario, form_: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarPerfilEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaPerfiles.delete(*self.tablaPerfiles.get_children())

            if where is not None and len(where) > 0:
                self.ListaPerfiles = consulPerfiles(where)
            else:
                self.ListaPerfiles = listarPerfil()
                self.ListaPerfiles.reverse()

            for p in self.ListaPerfiles:
                self.tablaPerfiles.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarPerfilEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            