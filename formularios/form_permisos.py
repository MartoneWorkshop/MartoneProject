import tkinter as tk
from config import  COLOR_FONDO, COLOR_MENU_LATERAL
import customtkinter
from util.util_alerts import set_opacity
from functions.conexion import ConexionDB
import datetime
import sqlite3
import traceback
from tkinter import ttk
from PIL import Image, ImageTk
from util.util_functions import ObtenerModulos, buscarCodigoModulo, actualizarCodigoModulo
from functions.PermDao import Permisos, listarPermisos, consulPermisos, SavePermiso, EditPermiso, PermisoDisable
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


class FormPermisos():
    def __init__(self, cuerpo_principal, permisos):
        self.id = None
        idmod = None
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

        self.buttonEditPerm = tk.Button(self.marco_permisos, text="Editar\n Permiso", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, 
                                        fg="white", anchor="w", compound=tk.LEFT, padx=10, 
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

        self.tablapermisos = ttk.Treeview(self.marco_permisos, column=('idmod','name','codperm','data_created','data_update'), height=25)
        self.tablapermisos.place(x=145, y=200)

        self.scroll = ttk.Scrollbar(self.marco_permisos, orient='vertical', command=self.tablapermisos.yview)
        self.scroll.place(x=893, y=200, height=526)
        self.tablapermisos.configure(yscrollcommand=self.scroll.set)
        self.tablapermisos.tag_configure('evenrow')

        self.tablapermisos.heading('#0',text="id")
        self.tablapermisos.heading('#1',text="idmod")
        self.tablapermisos.heading('#2',text="name")
        self.tablapermisos.heading('#3',text="codperm")
        self.tablapermisos.heading('#4',text="Date-C")
        self.tablapermisos.heading('#5',text="Date-U")

        self.tablapermisos.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablapermisos.column("#1", width=60, stretch=False)
        self.tablapermisos.column("#2", width=125, stretch=False)
        self.tablapermisos.column("#3", width=125, stretch=False)
        self.tablapermisos.column("#4", width=125, stretch=False)
        self.tablapermisos.column("#5", width=125, stretch=False)

        for p in self.Listapermisos:
            self.tablapermisos.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5]))
        
        self.tablapermisos.bind('<Double-1>', lambda event: self.editar_permiso(event, self.tablapermisos.item(self.tablapermisos.selection())['values']))

   # def update_client_content(self, event=None):
   # # Conectar a la base de datos
   #     self.connection = sqlite3.connect('database/database.db')
   #     self.cursor = self.connection.cursor()
   # # Obtener el contenido del Entry
   #     self.content = self.entrysearch_permisos.get()
   # # Realizar la consulta
   #     self.cursor.execute("""SELECT * FROM permisos WHERE
   #                     id LIKE ? OR 
   #                     coduser LIKE ? OR 
   #                     username LIKE ? OR 
   #                     pass LIKE ? OR 
   #                     idrol LIKE ? OR 
   #                     date_created LIKE ? OR
   #                     date_update LIKE ?""", 
   #                     ('%' + self.content + '%',
   #                     '%' + self.content + '%',  
   #                     '%' + self.content + '%',
   #                     '%' + self.content.strip() + '%',
   #                     '%' + self.content.strip() + '%',
   #                     '%' + self.content.strip() + '%', 
   #                     '%' + self.content.strip() + '%'))
   #     self.result = self.cursor.fetchall()
   # # Filtrar los registros según el contenido ingresado
   #     filtered_results = []
   #     for p in self.Listapermisos:
   #         if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              
   #             filtered_results.append(p)
#
   # # Borrar los elementos existentes en la tablaEquipos
   #     self.tablapermisos.delete(*self.tablapermisos.get_children())
#
   # # Insertar los nuevos resultados en la tablaEquipos
   #     for p in filtered_results:
   #         self.tablapermisos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
   #     self.cursor.close()
   #     self.connection.close()


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
        
        #Centrar l ventana en la pantalla
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

        modulos = ObtenerModulos()
        self.svmodulo_var = customtkinter.StringVar(value="Selecciona un modulo")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearpermisos, values=[modulo[1] for modulo in modulos], variable=self.svmodulo_var, command=lambda v: self.habilitar_entry(v))
        self.multioption.place(x=40, y=120)
        
        

        ############# NOMBRE DEL permiso
        self.lblnombrePerm = customtkinter.CTkLabel(self.topCreatePerm, text='Descripcion', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblnombrePerm.place(x=285, y=120) 
        
        self.svnombre_perm = customtkinter.StringVar()        
        self.entrynombre_perm = ttk.Entry(self.topCreatePerm, style='permern.TEntry', textvariable=self.svnombre_perm, state='disabled')        
        self.entrynombre_perm.place(x=255, y=150)       
        self.entrynombre_perm.configure(style='Entry.TEntry')
        
        ############# NOMBRE DEL ALIAS
        self.lblcodpermiso = customtkinter.CTkLabel(self.topCreatePerm, text='Alias del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblcodpermiso.place(x=420, y=120)
#
        self.svcodpermiso = customtkinter.StringVar()
        self.entrycodpermiso = ttk.Entry(self.topCreatePerm, style='permern.TEntry', textvariable=self.svcodpermiso, state='disabled')
        self.entrycodpermiso.place(x=405, y=150)
        self.entrycodpermiso.configure(style='Entry.TEntry')


        ######### BOTONE
        self.buttonSaveperm = tk.Button(self.topCreatePerm, text="Crear permiso", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarPermiso)
        self.buttonSaveperm.place(x=240, y=290)

    def habilitar_entry(self, _):
        self.opcion_seleccionada = self.svmodulo_var.get()
        if self.opcion_seleccionada != "Selecciona un modulo":
            self.entrynombre_perm.configure(state='normal')
            codpermiso = buscarCodigoModulo(self.opcion_seleccionada)
            codigo_permiso = f"{self.opcion_seleccionada.upper()[:4]}{codpermiso + 1}"
            self.svcodpermiso.set(codigo_permiso)
        else:
            self.entrynombre_perm.configure(state='disabled')
            self.svcodpermiso.set("")

    def editar_permiso(self, permisos, values):
        #Creacion del top level
        self.topEditperm = customtkinter.CTkToplevel()
        self.topEditperm.title("Editar permiso")
        self.topEditperm.w = 600
        self.topEditperm.h = 400
        self.topEditperm.geometry(f"{self.topEditperm.w}x{self.topEditperm.h}")
        self.topEditperm.resizable(False, False)
        self.topEditperm.configure(bg_color='#6a717e')
        self.topEditperm.configure(fg_color='#6a717e')

        self.idEdit = self.tablapermisos.item(self.tablapermisos.selection())['text']
        self.idmod = self.tablapermisos.item(self.tablapermisos.selection())['values'][0]
        self.nombre_permedit = self.tablapermisos.item(self.tablapermisos.selection())['values'][1]
        self.codperm = self.tablapermisos.item(self.tablapermisos.selection())['values'][2]

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

        self.lblinfo = customtkinter.CTkLabel(marco_editarpermisos, text="Editar permiso", font=("Roboto",14), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblinfo.place(x=220, rely=0.1)

        ############ NOMBRE DEL ALIAS
        self.lblnombrePerm = customtkinter.CTkLabel(marco_editarpermisos, text='Descripcion del permiso', font=("Roboto", 13), bg_color='#e1e3e5', fg_color='#e1e3e5')
        self.lblnombrePerm.place(x=255, y=120)

        self.svnombre_perm = customtkinter.StringVar(value=self.nombre_permedit)
        self.entrynombre_perm = ttk.Entry(marco_editarpermisos, style='permern.TEntry', textvariable=self.svnombre_perm)
        self.entrynombre_perm.place(x=240, y=170)
        self.entrynombre_perm.configure(style='Entry.TEntry')

        self.entrynombre_perm.bind("<Return>", lambda event: self.GuardarPermiso())
        ######## BOTONE
        self.buttonEditperm = tk.Button(marco_editarpermisos, text="Actualizar", font=("Roboto", 12),
                                        bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                        compound=tk.LEFT, padx=10, command=lambda: self.GuardarPermiso())
        self.buttonEditperm.place(x=240, y=290)

    

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

    
    def GuardarPermiso(self):
        try:
            # Otener el contenido del Entry
            
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
            idmodulo = None
            for modul in ObtenerModulos():
                if modul[1] == self.svmodulo_var.get():
                    idmodulo = modul[0]
                    break
            permisos = Permisos(
                idmodulo,
                self.svnombre_perm.get(),
                self.svcodpermiso.get(),
                date_created,
                date_update
            )
            if self.id is None:
                actualizarCodigoModulo(self.svmodulo_var.get())
                SavePermiso(permisos)
                self.topCreatePerm.destroy()
            else:
                EditPermiso(permisos, self.id)
                self.topEditperm.destroy()

            self.listarpermisoEnTabla()
        except Exception as e:
            error_advice()
            fecha_hora_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            mensaje = f'Error en GuardarPermiso, FormPermisos: {str(e)}'
            mensaje += f'Fecha y hora: {fecha_hora_actual}\n'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            