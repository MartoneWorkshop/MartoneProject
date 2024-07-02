import tkinter as tk
from tkinter import ttk, OptionMenu, Tk, Menu
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import customtkinter
import PIL
from PIL import Image, ImageTk
from tkinter import messagebox
from util.util_alerts import edit_advice, error_advice, save_advice, set_opacity
from functions.conexion import ConexionDB
from util.util_functions import obtener_permisos, ObtenerListaDeModulos, ObtenerPermisosDeModulos, ObtenerRoles, buscarCorrelativo, actualizarCorrelativo, ObtenerModulos
from functions.ProvDao import Proveedores, consulProv, listarProveedores, SaveProv, EditProv, ProvDisable, ProveedoresDesactivados
import sqlite3
import datetime
import ctypes



class FormProv():

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
            
        self.barra_inferior.bind("<Configure>", ajustar_imagen)
        
        bg = imagen_tk

        self.marco_prov = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_prov.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_prov, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateProv = tk.Button(self.marco_prov, text="Crear\n Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_proveedor(permisos, bg))
        self.buttonCreateProv.place(x=140, y=50)

        self.buttonEditProv = tk.Button(self.marco_prov, text="Editar\n Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_proveedor(permisos, self.tablaProveedores.item(self.tablaProveedores.selection())['values']))
        self.buttonEditProv.place(x=245, y=50)

        self.buttonDeleteProv = tk.Button(self.marco_prov, text="Desactivar\n Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.desactivarProveedor(permisos))
        self.buttonDeleteProv.place(x=350, y=50)
        
        self.switchStatus = tk.BooleanVar(value=True)
        self.switchPermStatus = customtkinter.CTkSwitch(self.marco_prov, variable=self.switchStatus, text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
        self.switchPermStatus.place(x=700, y=157)
    
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_proveedors = customtkinter.CTkLabel(self.marco_prov, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_proveedors.place(x=140, y=155)

        self.sventrysearch_proveedores = customtkinter.StringVar()
        self.entrysearch_proveedores = ttk.Entry(self.marco_prov, textvariable=self.sventrysearch_proveedores, style='Modern.TEntry', width=30)
        self.entrysearch_proveedores.place(x=175, y=157)
        self.entrysearch_proveedores.bind('<KeyRelease>', self.update_prov_content)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.ListaProveedores = consulProv(where)
        else:
            self.ListaProveedores = listarProveedores()
            self.ListaProveedores.reverse()

        self.tablaProveedores = ttk.Treeview(self.marco_prov, column=('coduser','username','password','idrol','data_create','data_update'), height=25)
        self.tablaProveedores.place(x=145, y=200)

        self.scroll = ttk.Scrollbar(self.marco_prov, orient='vertical', command=self.tablaProveedores.yview)
        self.scroll.place(x=890, y=200, height=526)

        self.tablaProveedores.configure(yscrollcommand=self.scroll.set)
        self.tablaProveedores.tag_configure('evenrow')

        self.tablaProveedores.heading('#0',text="ID")
        self.tablaProveedores.heading('#1',text="Coduser")
        self.tablaProveedores.heading('#2',text="Username")
        self.tablaProveedores.heading('#3',text="Contraseña")
        self.tablaProveedores.heading('#4',text="Perfil")
        self.tablaProveedores.heading('#5',text="Date-C")
        self.tablaProveedores.heading('#6',text="Date-U")

        self.tablaProveedores.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaProveedores.column("#1", width=60, stretch=False)
        self.tablaProveedores.column("#2", width=125, stretch=False)
        self.tablaProveedores.column("#3", width=125, stretch=False)
        self.tablaProveedores.column("#4", width=125, stretch=False)
        self.tablaProveedores.column("#5", width=124, stretch=False)
        self.tablaProveedores.column("#6", width=124, stretch=False)

        for p in self.ListaProveedores:
            self.tablaProveedores.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))

        self.tablaProveedores.bind('<Double-1>', lambda event: self.editar_proveedor(event, self.tablaProveedores.item(self.tablaProveedores.selection())['values']))
    
    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchPermStatus.configure(text="Activos")
            self.mostrarProveedoresActivos()
        else:
            self.switchPermStatus.configure(text="Inactivos")
            self.mostrarProveedoresDesactivados()

    def mostrarProveedoresActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaProveedores.delete(*self.tablaProveedores.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listarProveedores()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaProveedores.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6]))

    def mostrarProveedoresDesactivados(self):
        self.tablaProveedores.delete(*self.tablaProveedores.get_children())
        permisos_desactivados = ProveedoresDesactivados()
        for p in permisos_desactivados:
            self.tablaProveedores.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))

    def update_prov_content(self, event=None):
        conexion = ConexionDB()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_proveedores.get()
    # Realizar la consulta
        sql = """SELECT * FROM proveedores WHERE
                id LIKE ? OR 
                coduser LIKE ? OR 
                username LIKE ? OR 
                password LIKE ? OR 
                idrol LIKE ? OR 
                date_created LIKE ? OR
                date_update LIKE ?"""
        parametros = ('%' + self.content + '%',
                '%' + self.content + '%',  
                '%' + self.content + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%', 
                '%' + self.content.strip() + '%')
        conexion.ejecutar_consulta_parametros(sql, parametros)
        resultados = conexion.obtener_resultados()  
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.ListaProveedores:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaProveedores.delete(*self.tablaProveedores.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaProveedores.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        conexion.cerrarConexion()

    def crear_proveedor(self, permisos, bg):
        self.id = None
        #Creacion del top level
        self.topCreateProv = customtkinter.CTkToplevel()
        self.topCreateProv.title("Crear Proveedor")
        self.topCreateProv.w = 600
        self.topCreateProv.h = 400
        self.topCreateProv.geometry(f"{self.topCreateProv.w}x{self.topCreateProv.h}")
        self.topCreateProv.resizable(False, False)
        self.topCreateProv.configure(bg_color='#6a717e')
        self.topCreateProv.configure(fg_color='#6a717e')

        #Centrar la ventana en la pantalla
        screen_width = self.topCreateProv.winfo_screenwidth()
        screen_height = self.topCreateProv.winfo_screenheight()
        x = (screen_width - self.topCreateProv.w) // 2
        y = (screen_height - self.topCreateProv.h) // 2
        self.topCreateProv.geometry(f"+{x}+{y}")

        self.topCreateProv.lift()
        self.topCreateProv.grab_set()
        self.topCreateProv.transient()
        #Conversion de ico
        prov_ico = Image.open("imagenes/user.png")
        prov_ico = prov_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        prov_img = ImageTk.PhotoImage(prov_ico)

        pass_ico = Image.open("imagenes/pass.png")
        pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        pass_img = ImageTk.PhotoImage(pass_ico)

        selected_item = self.tablaProveedores.focus()
        values = self.tablaProveedores.item(selected_item)['values']
        #Datos para el proveedor
        marco_crearproveedor = customtkinter.CTkFrame(self.topCreateProv, width=550,height=350, bg_color="white", fg_color="white")
        marco_crearproveedor.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_crearproveedor, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_crearproveedor, text="Creacion de nuevo proveedor", font=("Roboto",14))
        self.lblinfo.place(x=205, rely=0.1)

        self.lblproveedor = customtkinter.CTkLabel(marco_crearproveedor, text='', image=prov_img, font=("Roboto", 14))
        self.lblproveedor.place(x=75, y=120)

        self.svproveedor = customtkinter.StringVar()
        self.entryproveedor = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svproveedor)
        self.entryproveedor.place(x=125, y=120)
        self.entryproveedor.configure(style='Entry.TEntry')

        #Datos de la Contraseña
        self.lblpassword = customtkinter.CTkLabel(marco_crearproveedor, text='', image=pass_img, font=("Roboto", 14))
        self.lblpassword.place(x=75, y=170)
        
        self.svpassword = customtkinter.StringVar()
        self.entrypassword = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svpassword, show='*')
        self.entrypassword.place(x=125, y=170)
        self.entrypassword.configure(style='Entry.TEntry')

        roles = ObtenerRoles()
        self.svperfil_var = customtkinter.StringVar(value="Selecciona un perfil")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearproveedor, values=[rol[1] for rol in roles], variable=self.svperfil_var)
        self.multioption.place(x=325, y=120)

        self.buttonCreate = tk.Button(marco_crearproveedor, text="Crear Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                        compound=tk.LEFT, padx=10, command=self.GuardarProveedor)
        self.buttonCreate.place(x=215, y=250)

    def editar_proveedor(self, permisos, values):
        if values:
    # Creación del top level
            self.id = self.tablaProveedores.item(self.tablaProveedores.selection())['text']
            self.proveedor = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][1]
            self.password = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][2]

            self.topEdit = customtkinter.CTkToplevel()
            self.topEdit.title("Editar Proveedor")
            self.topEdit.iconbitmap("imagenes/logo_ico.ico")
            self.topEdit.w = 600
            self.topEdit.h = 400
            self.topEdit.geometry(f"{self.topEdit.w}x{self.topEdit.h}")
            self.topEdit.resizable(False, False)
            self.topEdit.configure(bg_color='#6a717e')
            self.topEdit.configure(fg_color='#6a717e')


            # Centrar la ventana en la pantalla
            screen_width = self.topEdit.winfo_screenwidth()
            screen_height = self.topEdit.winfo_screenheight()
            x = (screen_width - self.topEdit.w) // 2
            y = (screen_height - self.topEdit.h) // 2
            self.topEdit.geometry(f"+{x}+{y}")

            self.topEdit.lift()
            self.topEdit.grab_set()
            self.topEdit.transient()

            # Conversion de ico
            prov_ico = Image.open("imagenes/user.png")
            prov_ico = prov_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
            prov_img = ImageTk.PhotoImage(prov_ico)

            pass_ico = Image.open("imagenes/pass.png")
            pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
            pass_img = ImageTk.PhotoImage(pass_ico)
            # Datos para el proveedor
            marco_editarproveedor = customtkinter.CTkFrame(self.topEdit, width=550, height=350, bg_color="white", fg_color="white")
            marco_editarproveedor.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(marco_editarproveedor, 0.8)

            self.lblinfo = customtkinter.CTkLabel(marco_editarproveedor, text="Edición de proveedor", font=("Roboto", 14))
            self.lblinfo.place(x=205, rely=0.1)

            self.lblproveedor = customtkinter.CTkLabel(marco_editarproveedor, text='', image=prov_img, font=("Roboto", 14))
            self.lblproveedor.place(x=75, y=120)

            self.svproveedor = customtkinter.StringVar(value=self.proveedor)  # Valor del proveedor a editar
            self.entryproveedor = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svproveedor)
            self.entryproveedor.place(x=125, y=120)
            self.entryproveedor.configure(style='Entry.TEntry')

            # Datos de la Contraseña
            self.lblpassword = customtkinter.CTkLabel(marco_editarproveedor, text='', image=pass_img, font=("Roboto", 14))
            self.lblpassword.place(x=75, y=170)

            self.svpassword = customtkinter.StringVar(value=self.password)  # Valor de la contraseña a editar
            self.entrypassword = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svpassword, show='*')
            self.entrypassword.place(x=125, y=170)
            self.entrypassword.configure(style='Entry.TEntry')

            perfil_id = values[3]
            perfil_nombre = ''
            for rol in ObtenerRoles():
                if rol[0] == perfil_id:
                    perfil_nombre = rol[1]
                    break
            self.svperfil_var = customtkinter.StringVar(value=perfil_nombre)  # Valor del perfil a editar
            self.multioption = customtkinter.CTkOptionMenu(marco_editarproveedor, values=[rol[1] for rol in ObtenerRoles()], variable=self.svperfil_var)
            self.multioption.place(x=325, y=120)

            self.buttonSave = tk.Button(marco_editarproveedor, text="Guardar Cambios", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                            compound=tk.LEFT, padx=10, command=self.GuardarProveedor)
            self.buttonSave.place(x=215, y=250)
        else:
            messagebox.showerror("Error", "Debe seleccionar un proveedor")

    def GuardarProveedor(self):
        try:
            # Otener el contenido del Entry
            coduser = buscarCorrelativo('proveedor')
            actualizarCorrelativo('proveedor')
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
            perfilname = self.svperfil_var.get()
            idperfil = None
            for rol in ObtenerRoles():
                if rol[1] == perfilname:
                    idperfil = rol[0]
                    break

            proveedor = Proveedores(
                coduser,
                self.svproveedor.get(),
                self.svpassword.get(),
                idperfil,
                date_created,
                date_update
            )
            if self.id is None:
                SaveProv(proveedor)
                self.topCreateProv.destroy()
            else:
                EditProv(proveedor, self.id)
                self.topEdit.destroy()

            self.listarProovedoresEnTabla()
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarProveedor, form_proveedores: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    
    def desactivarProveedor(self, permisos):
        try:
            self.id = self.tablaProveedores.item(self.tablaProveedores.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas Seguro de que deseas desactivar este proveedor?")
            if confirmar and 'CONF1011' in permisos:
                ProvDisable(self.id)
                self.listarProvedoresEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarProveedor, form_proveedores: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarProveedoresEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaProveedores.delete(*self.tablaProveedores.get_children())

            if where is not None and len(where) > 0:
                self.ListaProveedores = consulProv(where)
            else:
                self.ListaProveedores = listarProveedores()
                self.ListaProveedores.reverse()

            for p in self.ListaProveedores:
                self.tablaProveedores.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarProveedoresEnTabla, form_proveedores: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')





    