import tkinter as tk
from tkinter import ttk, OptionMenu, Tk, Menu
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import customtkinter
import PIL
from PIL import Image, ImageTk
from tkinter import messagebox
from util.util_alerts import edit_advice, error_advice, save_advice, set_opacity
from functions.conexion import ConexionDB
from util.old_functions import obtener_permisos, getModuleList, getModulePerm, ObtenerRoles, buscarCorrelativo, actualizarCorrelativo, getModule
from functions.UsersDao import user, searchUsers, listUsers, save_user, edit_user, userDisable, inactive_users
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
            
        self.barra_inferior.bind("<Configure>", adjustImage)
        
        bg = imagen_tk

        self.marco_create = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_create.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_create, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateUser = tk.Button(self.marco_create, text="Crear\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormCreateUser(permisos, bg))
        self.buttonCreateUser.place(x=140, y=50)

        self.buttonEditUser = tk.Button(self.marco_create, text="Editar\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormEditUser(permisos, self.usersTable.item(self.usersTable.selection())['values']))
        self.buttonEditUser.place(x=245, y=50)

        if 'CONF1006' in permisos:
            self.buttonDeleteUser = tk.Button(self.marco_create, text="Desactivar\n Usuario", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateUser(permisos))
            self.buttonDeleteUser.place(x=350, y=50)
        else: 
            self.buttonDeleteUser = tk.Button(self.marco_create, text="Desactivar\n Usuario", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateUser(permisos))
            self.buttonDeleteUser.place(x=350, y=50)

        if 'CONF1014' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchUserStatus = customtkinter.CTkSwitch(self.marco_create, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.SwitchStatus)
            self.switchUserStatus.place(x=700, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchUserStatus = customtkinter.CTkSwitch(self.marco_create, variable=self.switchStatus, state='disabled', text="Inactivos", font=("Roboto", 12), command=self.SwitchStatus)
            self.switchUserStatus.place(x=700, y=157)

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_users = customtkinter.CTkLabel(self.marco_create, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_users.place(x=140, y=155)

        self.sventrysearch_users = customtkinter.StringVar()
        self.entrysearch_users = ttk.Entry(self.marco_create, textvariable=self.sventrysearch_users, style='Modern.TEntry', width=30)
        self.entrysearch_users.place(x=175, y=157)
        self.entrysearch_users.bind('<KeyRelease>', self.updateSearch)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.userList = searchUsers(where)
        else:
            self.userList = listUsers()
            self.userList.reverse()

        self.usersTable = ttk.Treeview(self.marco_create, column=('coduser','username','password','idrol','data_create','data_update'), height=25)
        self.usersTable.place(x=145, y=200)

        self.scroll = ttk.Scrollbar(self.marco_create, orient='vertical', command=self.usersTable.yview)
        self.scroll.place(x=890, y=200, height=526)

        self.usersTable.configure(yscrollcommand=self.scroll.set)
        self.usersTable.tag_configure('evenrow')

        self.usersTable.heading('#0',text="ID")
        self.usersTable.heading('#1',text="Coduser")
        self.usersTable.heading('#2',text="Username")
        self.usersTable.heading('#3',text="Contraseña")
        self.usersTable.heading('#4',text="Perfil")
        self.usersTable.heading('#5',text="Date-C")
        self.usersTable.heading('#6',text="Date-U")

        self.usersTable.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.usersTable.column("#1", width=60, stretch=False)
        self.usersTable.column("#2", width=125, stretch=False)
        self.usersTable.column("#3", width=125, stretch=False)
        self.usersTable.column("#4", width=125, stretch=False)
        self.usersTable.column("#5", width=124, stretch=False)
        self.usersTable.column("#6", width=124, stretch=False)

        for p in self.userList:
            self.usersTable.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))

        self.usersTable.bind('<Double-1>', lambda event: self.FormEditUser(event, self.usersTable.item(self.usersTable.selection())['values']))
    
    def SwitchStatus(self):
        if self.switchStatus.get():
            self.switchUserStatus.configure(text="Activos")
            self.showActiveUsers()
        else:
            self.switchUserStatus.configure(text="Inactivos")
            self.showInactiveUsers()
    def showActiveUsers(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.usersTable.delete(*self.usersTable.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listUsers()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.usersTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6]))
    def showInactiveUsers(self):
        self.usersTable.delete(*self.usersTable.get_children())
        permisos_desactivados = inactive_users()
        for p in permisos_desactivados:
            self.usersTable.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))
    def updateSearch(self, event=None):
        conexion = ConexionDB()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_users.get()
    # Realizar la consulta
        sql = """SELECT * FROM users WHERE
                id LIKE ? OR 
                coduser LIKE ? OR 
                username LIKE ? OR 
                password LIKE ? OR 
                idrol LIKE ? OR 
                created_at LIKE ? OR
                updated_at LIKE ?"""
        parametros = ('%' + self.content + '%',
                '%' + self.content + '%',  
                '%' + self.content + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%', 
                '%' + self.content.strip() + '%')
        conexion.execute_consult_param(sql, parametros)
        resultados = conexion.get_results()  
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.userList:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.usersTable.delete(*self.usersTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.usersTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        conexion.closeConexion()
    def FormCreateUser(self, permisos, bg):
        self.id = None
        #Creacion del top level
        self.topCreateUser = customtkinter.CTkToplevel()
        self.topCreateUser.title("Crear users")
        self.topCreateUser.w = 600
        self.topCreateUser.h = 400
        self.topCreateUser.geometry(f"{self.topCreateUser.w}x{self.topCreateUser.h}")
        self.topCreateUser.resizable(False, False)
        self.topCreateUser.configure(bg_color='#6a717e')
        self.topCreateUser.configure(fg_color='#6a717e')


        #Centrar la ventana en la pantalla
        screen_width = self.topCreateUser.winfo_screenwidth()
        screen_height = self.topCreateUser.winfo_screenheight()
        x = (screen_width - self.topCreateUser.w) // 2
        y = (screen_height - self.topCreateUser.h) // 2
        self.topCreateUser.geometry(f"+{x}+{y}")

        self.topCreateUser.lift()
        self.topCreateUser.grab_set()
        self.topCreateUser.transient()
        #Conversion de ico
        user_ico = Image.open("imagenes/user.png")
        user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        user_img = ImageTk.PhotoImage(user_ico)

        pass_ico = Image.open("imagenes/pass.png")
        pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        pass_img = ImageTk.PhotoImage(pass_ico)

        selected_item = self.usersTable.focus()
        values = self.usersTable.item(selected_item)['values']
        #Datos para el usuario
        marco_crearusuario = customtkinter.CTkFrame(self.topCreateUser, width=550,height=350, bg_color="white", fg_color="white")
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
                                        compound=tk.LEFT, padx=10, command=self.SaveUser)
        self.buttonCreate.place(x=215, y=250)
    def FormEditUser(self, permisos, values):
        if values:
    # Creación del top level
            self.id = self.usersTable.item(self.usersTable.selection())['text']
            self.usuario = self.usersTable.item(self.usersTable.selection())['values'][1]
            self.password = self.usersTable.item(self.usersTable.selection())['values'][2]

            self.topEditUser = customtkinter.CTkToplevel()
            self.topEditUser.title("Editar Usuario")
            self.topEditUser.w = 600
            self.topEditUser.h = 400
            self.topEditUser.geometry(f"{self.topEditUser.w}x{self.topEditUser.h}")
            self.topEditUser.resizable(False, False)
            self.topEditUser.configure(bg_color='#6a717e')
            self.topEditUser.configure(fg_color='#6a717e')


            # Centrar la ventana en la pantalla
            screen_width = self.topEditUser.winfo_screenwidth()
            screen_height = self.topEditUser.winfo_screenheight()
            x = (screen_width - self.topEditUser.w) // 2
            y = (screen_height - self.topEditUser.h) // 2
            self.topEditUser.geometry(f"+{x}+{y}")

            self.topEditUser.lift()
            self.topEditUser.grab_set()
            self.topEditUser.transient()

            # Conversion de ico
            user_ico = Image.open("imagenes/icons/user.png")
            user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
            user_img = ImageTk.PhotoImage(user_ico)

            pass_ico = Image.open("imagenes/icons/pass.png")
            pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
            pass_img = ImageTk.PhotoImage(pass_ico)
            # Datos para el usuario
            marco_editarusuario = customtkinter.CTkFrame(self.topEditUser, width=550, height=350, bg_color="white", fg_color="white")
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
                                            compound=tk.LEFT, padx=10, command=self.SaveUser)
            self.buttonSave.place(x=215, y=250)
        else:
            messagebox.showerror("Error", "Debe seleccionar un usuario")
    def SaveUser(self):
        try:
            # Otener el contenido del Entry
            coduser = buscarCorrelativo('usuario')
            
            coduser = coduser + 1
            fecha_actual = datetime.datetime.now()
            created_at = fecha_actual.strftime("%Y-%M-%d")
            updated_at = fecha_actual.strftime("%Y-%M-%d %H:%M:%S")
            
            perfilname = self.svperfil_var.get()
            idperfil = None
            for rol in ObtenerRoles():
                if rol[1] == perfilname:
                    idperfil = rol[0]
                    break

            usuario = user(
                coduser,
                self.svusuario.get(),
                self.svpassword.get(),
                idperfil,
                created_at,
                updated_at,
                deleted_at = 'NULL'
            )
            if self.id is None:
                save_user(usuario)
                actualizarCorrelativo('usuario')
                self.topCreateUser.destroy()
            else:
                edit_user(usuario, self.id)
                self.topEditUser.destroy()
            self.UpdateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en SaveUser, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    def inactivateUser(self, permisos):
        try:
            self.id = self.usersTable.item(self.usersTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas Seguro de que deseas desactivar este usuario?")

            if confirmar:
                userDisable(self.id)
                self.UpdateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en inactivateUser, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    def UpdateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.usersTable.delete(*self.usersTable.get_children())

            if where is not None and len(where) > 0:
                self.listaCliente = searchUsers(where)
            else:
                self.listaCliente = listUsers()
                self.listaCliente.reverse()

            for p in self.listaCliente:
                self.usersTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en UpdateTable, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')





    