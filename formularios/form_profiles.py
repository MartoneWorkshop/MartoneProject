import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity, save_advice, edit_advice, error_advice, delete_advice
import traceback
from functions.conexion import ConexionDB
import datetime
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk
from functions.ProfileDao import Roles, listProfiles, searchProfiles, save_profile, edit_profile, ProfileDisable, update_Permiss, InactiveProfiles,saveNewPermiss, cleanPermiss
from util.old_functions import obtener_permisos, getModuleList, getModulePerm, ObtenerRoles, getModule, getAsignedPerm
from config import WIDTH_LOGO, HEIGHT_LOGO


class FormProfiles():

    def __init__(self, cuerpo_principal, permisos):
        self.id = None
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

        self.frame_profiles = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.frame_profiles.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.frame_profiles, 0.8)
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_perfiles = customtkinter.CTkLabel(self.frame_profiles, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_perfiles.place(x=220, y=155)

        self.sventrysearch_perfiles = customtkinter.StringVar()
        self.entrysearch_perfiles = ttk.Entry(self.frame_profiles, textvariable=self.sventrysearch_perfiles, style='Modern.TEntry', width=30)
        self.entrysearch_perfiles.place(x=270, y=157)
        self.entrysearch_perfiles.bind('<KeyRelease>', self.updateSearch)

        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateProfile = tk.Button(self.frame_profiles, text="Creacion de\nPerfiles", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormCreateProfiles(permisos))
        self.buttonCreateProfile.place(x=225, y=60)

        self.buttonEditProfile = tk.Button(self.frame_profiles, text="Edicion de\nPerfil", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormEditProfiles(permisos, self.profileTable.item(self.profileTable.selection())['values'])) 
        self.buttonEditProfile.place(x=355, y=60)

        if 'CONF1007' in permisos:
            self.buttonDeleteProfile = tk.Button(self.frame_profiles, text="Desactivar\n Perfil", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateProfile(permisos))
            self.buttonDeleteProfile.place(x=475, y=60)
        else:
            self.buttonDeleteProfile = tk.Button(self.frame_profiles, text="Desactivar\n Perfil", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateProfile(permisos))
            self.buttonDeleteProfile.place(x=475, y=60)

        if 'CONF1008' in permisos:
            self.buttonModPerm = tk.Button(self.frame_profiles, text="Modificar\n Permisos", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.modPermiss(permisos, self.profileTable.item(self.profileTable.selection())['values']))
            self.buttonModPerm.place(x=600, y=60)
        else:
            self.buttonModPerm = tk.Button(self.frame_profiles, text="Modificar\n Permisos", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.modPermiss(permisos, self.profileTable.item(self.profileTable.selection())['values']))
            self.buttonModPerm.place(x=600, y=60)

        if 'CONF1012' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchPermStatus = customtkinter.CTkSwitch(self.frame_profiles, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.showStatus)
            self.switchPermStatus.place(x=700, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchPermStatus = customtkinter.CTkSwitch(self.frame_profiles, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.showStatus)
            self.switchPermStatus.place(x=700, y=157)

        ###################################### Tabla de modulos activos ######################
        where = ""
        if len(where) > 0:
            self.profileList = searchProfiles(where)
        else:
            self.profileList = listProfiles()
            self.profileList.reverse()

        self.profileTable = ttk.Treeview(self.frame_profiles, column=('Nombre','Data_create','Data_update'), height=25)
        self.profileTable.place(x=210, y=200)

        self.scroll = ttk.Scrollbar(self.frame_profiles, orient='vertical', command=self.profileTable.yview)
        self.scroll.place(x=832, y=200, height=526)
        self.profileTable.configure(yscrollcommand=self.scroll.set)
        self.profileTable.tag_configure('evenrow')

        self.profileTable.heading('#0',text="ID")
        self.profileTable.heading('#1',text="Nombre")
        self.profileTable.heading('#2',text="Date-C")
        self.profileTable.heading('#3',text="Date-U")

        self.profileTable.column("#0", width=100, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.profileTable.column("#1", width=170, stretch=False)
        self.profileTable.column("#2", width=175, stretch=False)
        self.profileTable.column("#3", width=175, stretch=False)

        
        #self.tablaPerfiles.bind('<Double-1>', self.crear_usuario)
        for p in self.profileList:
            self.profileTable.insert('',0,text=p[0], values=(p[1],p[2],p[3]))
        
        
        self.profileTable.bind('<Double-1>', lambda event: self.FormEditProfiles(event, self.profileTable.item(self.profileTable.selection())['values']))
    
    def showStatus(self):
        if self.switchStatus.get():
            self.switchPermStatus.configure(text="Activos")
            self.showActive()
        else:
            self.switchPermStatus.configure(text="Inactivos")
            self.showInactive()

    def showActive(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.profileTable.delete(*self.profileTable.get_children())
        # Obtener la lista de permisos activos
        activeProfiles = listProfiles()
        # Insertar los permisos activos en la tabla
        for p in activeProfiles:
            self.profileTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))

    def showInactive(self):
        self.profileTable.delete(*self.profileTable.get_children())
        permisos_desactivados = InactiveProfiles()
        for p in permisos_desactivados:
            self.profileTable.insert('',0, text=p[0], values=(p[1],p[2],p[3]))

    def updateSearch(self, event=None):
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
        for p in self.profileList:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.profileTable.delete(*self.profileTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.profileTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
        self.cursor.close()
        self.connection.close()


    def FormCreateProfiles(self, permisos):
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

        frame_createProfile = customtkinter.CTkFrame(self.topCreateProfile, width=550,height=350, bg_color="white", fg_color="white")
        frame_createProfile.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(frame_createProfile, 0.8)

        self.lblinfo = customtkinter.CTkLabel(self.topCreateProfile, text="Creacion de un nuevo Perfil", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############# NOMBRE DEL MODULO
        self.lblnombre = customtkinter.CTkLabel(self.topCreateProfile, text='Nombre del Perfil', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblnombre.place(relx=0.42, y=120)

        self.svnombre_perfil = customtkinter.StringVar()
        self.entrynombre_perfil = ttk.Entry(self.topCreateProfile, style='Modern.TEntry', textvariable=self.svnombre_perfil)
        self.entrynombre_perfil.place(relx=0.4, y=170)
        self.entrynombre_perfil.configure(style='Entry.TEntry')

    
        self.entrynombre_perfil.bind("<Return>", lambda event: self.SaveProfile())
        ######## BOTONE
        self.buttonSaveProfile = tk.Button(self.topCreateProfile, text="Crear Perfil", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.SaveProfile)
        self.buttonSaveProfile.place(x=240, y=290)


    def FormEditProfiles(self, permisos, values):
        if values:
            self.id = self.profileTable.item(self.profileTable.selection())['text']
            self.nombredit = self.profileTable.item(self.profileTable.selection())['values'][0]
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

            frame_editProfile = customtkinter.CTkFrame(self.topEditProfile, width=550,height=350, bg_color="white", fg_color="white")
            frame_editProfile.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(frame_editProfile, 0.8)

            self.lblinfo = customtkinter.CTkLabel(self.topEditProfile, text="Editar Perfil", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
            self.lblinfo.place(relx=0.43, rely=0.1)

            ############# NOMBRE DEL MODULO
            self.lbleditnombre = customtkinter.CTkLabel(self.topEditProfile, text='Nombre del Perfil', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
            self.lbleditnombre.place(relx=0.42, y=120)

            self.svnombre_perfil = customtkinter.StringVar(value=self.nombredit)
            self.entryeditnombre_perfil = ttk.Entry(self.topEditProfile, style='Modern.TEntry', textvariable=self.svnombre_perfil)
            self.entryeditnombre_perfil.place(relx=0.4, y=170)
            self.entryeditnombre_perfil.configure(style='Entry.TEntry')

            self.entryeditnombre_perfil.bind("<Return>", lambda event: self.SaveProfile())
            ######## BOTONE
            self.buttonEditProfile = tk.Button(self.topEditProfile, text="Actualizar", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.SaveProfile)
            self.buttonEditProfile.place(x=250, y=290)
        else:
            messagebox.showerror("Error", "Debe seleccionar un perfil")


    def modPermiss(self, permisos, values):
        if values:
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
            perfil_id = self.profileTable.item(self.profileTable.selection())['text'] 
            modulos = getModuleList()
            asigperm = getAsignedPerm(perfil_id)
            self.tabs = {}
            interruptores = {}
            for modulo in modulos:
                nombre_modulo = modulo['name']
                tab = self.tab_permisos.add(nombre_modulo)
                self.tabs[nombre_modulo] = tab
                if modulo == 'Home':
                    self.tab_permisos.set(tab)
                id_modulo = modulo['id']
                permisos_modulo = getModulePerm(id_modulo)
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
                                            padx=10, command=lambda: self.updatePerm(perfil_id, interruptores))
            self.buttonActualizar.place(x=323, y=515)
        else:
            messagebox.showerror("Error", "Debe seleccionar un perfil")

    def saveSelectedPerm(self, interruptores):
        try:
            permisos_seleccionados = [permiso['codperm'] for interruptor, permiso in interruptores.items() if permiso.get('codperm') and interruptor.get()]
            return permisos_seleccionados

        except Exception as e:
            error_advice()
            mensaje = f'Error en saveSelectedPerm, form_Perfiles: {str(e)}'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    
    def updatePerm(self, perfil_id, interruptores):
        try:
            permisos_seleccionados = self.saveSelectedPerm(interruptores)
            cleanPermiss(perfil_id)
            
            saveNewPermiss(perfil_id, permisos_seleccionados)
            self.topModperm.destroy()
        except Exception as e:
            error_advice()
            mensaje = f'Error en updatePerm, form_Perfiles: {str(e)}'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    
    def SaveProfile(self):
        try:
            # Otener el contenido del Entry
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%Y-%M-%d")
            date_update = fecha_actual.strftime("%Y-%M-%d %H:%M:%S")
    
            roles = Roles(
                self.svnombre_perfil.get(),
                date_created,
                date_update
            )
            if self.id is None:
                save_profile(roles)
                self.topCreateProfile.destroy()
            else:
                edit_profile(roles, self.id)
                self.topEditProfile.destroy()
            self.updateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en SaveProfile, form_Perfiles: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def inactivateProfile(self, permisos):
        try:
            self.id = self.profileTable.item(self.profileTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este perfil?")
            if confirmar and 'CONF1007' in permisos:
                ProfileDisable(self.id)
                self.updateTable()
            else:
                messagebox.showerror("Error", "No posee permisos suficientes para realizar esta accion.")
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en inactiveProfile, form_profiles: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def updateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.profileTable.delete(*self.profileTable.get_children())

            if where is not None and len(where) > 0:
                self.profileList = searchProfiles(where)
            else:
                self.profileList = listProfiles()
                self.profileList.reverse()

            for p in self.profileList:
                self.profileTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en updateTable, form_profiles: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            