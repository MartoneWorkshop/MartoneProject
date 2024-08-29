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
from functions.UsersDao import usuarios, consulUsers, listarUsuarios, SaveUser, EditUser, UserDisable, UsuariosDesactivados
import sqlite3
import datetime
import ctypes



class FormUsers():

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

        self.marco_create = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_create.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_create, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateUser = tk.Button(self.marco_create, text="Crear\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_usuario(permisos, bg))
        self.buttonCreateUser.place(x=140, y=50)

        self.buttonEditUser = tk.Button(self.marco_create, text="Editar\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_usuario(permisos, self.tablaUsuarios.item(self.tablaUsuarios.selection())['values']))
        self.buttonEditUser.place(x=245, y=50)

        if 'CONF1006' in permisos:
            self.buttonDeleteUser = tk.Button(self.marco_create, text="Desactivar\n Usuario", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarUsuario(permisos))
            self.buttonDeleteUser.place(x=350, y=50)
        else: 
            self.buttonDeleteUser = tk.Button(self.marco_create, text="Desactivar\n Usuario", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarUsuario(permisos))
            self.buttonDeleteUser.place(x=350, y=50)

        if 'CONF1014' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchUserStatus = customtkinter.CTkSwitch(self.marco_create, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchUserStatus.place(x=700, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchUserStatus = customtkinter.CTkSwitch(self.marco_create, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchUserStatus.place(x=700, y=157)

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_usuarios = customtkinter.CTkLabel(self.marco_create, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_usuarios.place(x=140, y=155)

        self.sventrysearch_usuarios = customtkinter.StringVar()
        self.entrysearch_usuarios = ttk.Entry(self.marco_create, textvariable=self.sventrysearch_usuarios, style='Modern.TEntry', width=30)
        self.entrysearch_usuarios.place(x=175, y=157)
        self.entrysearch_usuarios.bind('<KeyRelease>', self.update_users_content)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.ListaUsuarios = consulUsers(where)
        else:
            self.ListaUsuarios = listarUsuarios()
            self.ListaUsuarios.reverse()

        self.tablaUsuarios = ttk.Treeview(self.marco_create, column=('coduser','username','password','idrol','data_create','data_update'), height=25)
        self.tablaUsuarios.place(x=145, y=200)

        self.scroll = ttk.Scrollbar(self.marco_create, orient='vertical', command=self.tablaUsuarios.yview)
        self.scroll.place(x=890, y=200, height=526)

        self.tablaUsuarios.configure(yscrollcommand=self.scroll.set)
        self.tablaUsuarios.tag_configure('evenrow')

        self.tablaUsuarios.heading('#0',text="ID")
        self.tablaUsuarios.heading('#1',text="Coduser")
        self.tablaUsuarios.heading('#2',text="Username")
        self.tablaUsuarios.heading('#3',text="Contraseña")
        self.tablaUsuarios.heading('#4',text="Perfil")
        self.tablaUsuarios.heading('#5',text="Date-C")
        self.tablaUsuarios.heading('#6',text="Date-U")

        self.tablaUsuarios.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaUsuarios.column("#1", width=60, stretch=False)
        self.tablaUsuarios.column("#2", width=125, stretch=False)
        self.tablaUsuarios.column("#3", width=125, stretch=False)
        self.tablaUsuarios.column("#4", width=125, stretch=False)
        self.tablaUsuarios.column("#5", width=124, stretch=False)
        self.tablaUsuarios.column("#6", width=124, stretch=False)

        for p in self.ListaUsuarios:
            self.tablaUsuarios.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))

        self.tablaUsuarios.bind('<Double-1>', lambda event: self.editar_usuario(event, self.tablaUsuarios.item(self.tablaUsuarios.selection())['values']))
    
    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchUserStatus.configure(text="Activos")
            self.mostrarUsuariosActivos()
        else:
            self.switchUserStatus.configure(text="Inactivos")
            self.mostrarUsuariosDesactivados()

    def mostrarUsuariosActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaUsuarios.delete(*self.tablaUsuarios.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listarUsuarios()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaUsuarios.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6]))

    def mostrarUsuariosDesactivados(self):
        self.tablaUsuarios.delete(*self.tablaUsuarios.get_children())
        permisos_desactivados = UsuariosDesactivados()
        for p in permisos_desactivados:
            self.tablaUsuarios.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))

    def update_users_content(self, event=None):
        conexion = ConexionDB()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_usuarios.get()
    # Realizar la consulta
        sql = """SELECT * FROM usuarios WHERE
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
        for p in self.ListaUsuarios:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaUsuarios.delete(*self.tablaUsuarios.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaUsuarios.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        conexion.cerrarConexion()

    def crear_usuario(self, permisos, bg):
        self.id = None
        #Creacion del top level
        self.topCreate = customtkinter.CTkToplevel()
        self.topCreate.title("Crear Usuarios")
        self.topCreate.w = 600
        self.topCreate.h = 400
        self.topCreate.geometry(f"{self.topCreate.w}x{self.topCreate.h}")
        self.topCreate.resizable(False, False)
        self.topCreate.configure(bg_color='#6a717e')
        self.topCreate.configure(fg_color='#6a717e')


        #Centrar la ventana en la pantalla
        screen_width = self.topCreate.winfo_screenwidth()
        screen_height = self.topCreate.winfo_screenheight()
        x = (screen_width - self.topCreate.w) // 2
        y = (screen_height - self.topCreate.h) // 2
        self.topCreate.geometry(f"+{x}+{y}")

        self.topCreate.lift()
        self.topCreate.grab_set()
        self.topCreate.transient()
        #Conversion de ico
        user_ico = Image.open("imagenes/user.png")
        user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        user_img = ImageTk.PhotoImage(user_ico)

        pass_ico = Image.open("imagenes/pass.png")
        pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        pass_img = ImageTk.PhotoImage(pass_ico)

        selected_item = self.tablaUsuarios.focus()
        values = self.tablaUsuarios.item(selected_item)['values']
        #Datos para el usuario
        marco_crearusuario = customtkinter.CTkFrame(self.topCreate, width=550,height=350, bg_color="white", fg_color="white")
        marco_crearusuario.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_crearusuario, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_crearusuario, text="Creacion de nuevo usuario", font=("Roboto",14))
        self.lblinfo.place(x=205, rely=0.1)
        
        self.lblusuario = customtkinter.CTkLabel(marco_crearusuario, text='', image=user_img, font=("Roboto", 14))
        self.lblusuario.place(x=75, y=120)

        self.svusuario = customtkinter.StringVar()
        self.entryusuario = ttk.Entry(marco_crearusuario, style='Modern.TEntry', textvariable=self.svusuario)
        self.entryusuario.place(x=125, y=120)
        self.entryusuario.configure(style='Entry.TEntry')

        #Datos de la Contraseña
        self.lblpassword = customtkinter.CTkLabel(marco_crearusuario, text='', image=pass_img, font=("Roboto", 14))
        self.lblpassword.place(x=75, y=170)
        
        self.svpassword = customtkinter.StringVar()
        self.entrypassword = ttk.Entry(marco_crearusuario, style='Modern.TEntry', textvariable=self.svpassword, show='*')
        self.entrypassword.place(x=125, y=170)
        self.entrypassword.configure(style='Entry.TEntry')

        roles = ObtenerRoles()
        self.svperfil_var = customtkinter.StringVar(value="Selecciona un perfil")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearusuario, values=[rol[1] for rol in roles], variable=self.svperfil_var)
        self.multioption.place(x=325, y=120)

        self.buttonCreate = tk.Button(marco_crearusuario, text="Crear Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                        compound=tk.LEFT, padx=10, command=self.GuardarUsuario)
        self.buttonCreate.place(x=215, y=250)

    def editar_usuario(self, permisos, values):
        if values:
    # Creación del top level
            self.id = self.tablaUsuarios.item(self.tablaUsuarios.selection())['text']
            self.usuario = self.tablaUsuarios.item(self.tablaUsuarios.selection())['values'][1]
            self.password = self.tablaUsuarios.item(self.tablaUsuarios.selection())['values'][2]

            self.topEdit = customtkinter.CTkToplevel()
            self.topEdit.title("Editar Usuario")
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
            user_ico = Image.open("imagenes/icons/user.png")
            user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
            user_img = ImageTk.PhotoImage(user_ico)

            pass_ico = Image.open("imagenes/icons/pass.png")
            pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
            pass_img = ImageTk.PhotoImage(pass_ico)
            # Datos para el usuario
            marco_editarusuario = customtkinter.CTkFrame(self.topEdit, width=550, height=350, bg_color="white", fg_color="white")
            marco_editarusuario.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(marco_editarusuario, 0.8)

            self.lblinfo = customtkinter.CTkLabel(marco_editarusuario, text="Edición de usuario", font=("Roboto", 14))
            self.lblinfo.place(x=205, rely=0.1)

            self.lblusuario = customtkinter.CTkLabel(marco_editarusuario, text='', image=user_img, font=("Roboto", 14))
            self.lblusuario.place(x=75, y=120)

            self.svusuario = customtkinter.StringVar(value=self.usuario)  # Valor del usuario a editar
            self.entryusuario = ttk.Entry(marco_editarusuario, style='Modern.TEntry', textvariable=self.svusuario)
            self.entryusuario.place(x=125, y=120)
            self.entryusuario.configure(style='Entry.TEntry')

            # Datos de la Contraseña
            self.lblpassword = customtkinter.CTkLabel(marco_editarusuario, text='', image=pass_img, font=("Roboto", 14))
            self.lblpassword.place(x=75, y=170)

            self.svpassword = customtkinter.StringVar(value=self.password)  # Valor de la contraseña a editar
            self.entrypassword = ttk.Entry(marco_editarusuario, style='Modern.TEntry', textvariable=self.svpassword, show='*')
            self.entrypassword.place(x=125, y=170)
            self.entrypassword.configure(style='Entry.TEntry')

            perfil_id = values[3]
            perfil_nombre = ''
            for rol in ObtenerRoles():
                if rol[0] == perfil_id:
                    perfil_nombre = rol[1]
                    break
            self.svperfil_var = customtkinter.StringVar(value=perfil_nombre)  # Valor del perfil a editar
            self.multioption = customtkinter.CTkOptionMenu(marco_editarusuario, values=[rol[1] for rol in ObtenerRoles()], variable=self.svperfil_var)
            self.multioption.place(x=325, y=120)

            self.buttonSave = tk.Button(marco_editarusuario, text="Guardar Cambios", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                            compound=tk.LEFT, padx=10, command=self.GuardarUsuario)
            self.buttonSave.place(x=215, y=250)
        else:
            messagebox.showerror("Error", "Debe seleccionar un usuario")

    def GuardarUsuario(self):
        try:
            # Otener el contenido del Entry
            coduser = buscarCorrelativo('usuario')
            
            coduser = coduser + 1
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
            perfilname = self.svperfil_var.get()
            idperfil = None
            for rol in ObtenerRoles():
                if rol[1] == perfilname:
                    idperfil = rol[0]
                    break

            usuario = usuarios(
                coduser,
                self.svusuario.get(),
                self.svpassword.get(),
                idperfil,
                date_created,
                date_update
            )
            if self.id is None:
                SaveUser(usuario)
                actualizarCorrelativo('usuario')
                self.topCreate.destroy()
            else:
                EditUser(usuario, self.id)
                self.topEdit.destroy()
            self.listarUsuariosEnTabla()

        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    
    def desactivarUsuario(self, permisos):
        try:
            self.id = self.tablaUsuarios.item(self.tablaUsuarios.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas Seguro de que deseas desactivar este usuario?")

            if confirmar:
                UserDisable(self.id)
                self.listarUsuariosEnTabla()

        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarUsuariosEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaUsuarios.delete(*self.tablaUsuarios.get_children())

            if where is not None and len(where) > 0:
                self.listaCliente = consulUsers(where)
            else:
                self.listaCliente = listarUsuarios()
                self.listaCliente.reverse()

            for p in self.listaCliente:
                self.tablaUsuarios.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarUsuariosEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')





    