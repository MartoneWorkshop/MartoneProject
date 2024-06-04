import tkinter as tk
from tkinter import ttk, OptionMenu, Tk, Menu
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import customtkinter
import PIL
from PIL import Image, ImageTk
from util.util_alerts import edit_advice, error_advice, save_advice, set_opacity
from functions.UsersDao import usuarios, consulUsers, listarUsuarios, SaveUser, EditUser
import sqlite3
import datetime


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
        ruta_imagen = "imagenes/bg.jpg"
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
            
        cuerpo_principal.bind("<Configure>", ajustar_imagen)
        
        self.marco_create = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_create.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_create, 0.8)

        #self.label_accion = customtkinter.CTkLabel(self.self.marco_create, text="Selector de Acciones para Usuarios", font=("Roboto", 15))
        #self.label_accion.place(x=50, y=50)
        #self.optionmenu_var = customtkinter.StringVar(value="Accion a Ejecutar")
        #self.optionmenu = customtkinter.CTkOptionMenu(self.self.marco_create,values=["Crear Usuario", "Editar Usuario", "Desactivar Usuario"],
        #                                variable=self.optionmenu_var, width=220,height=45, font=("Roboto", 15))
        #self.optionmenu.place(x=60, y=100)
        ###################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateUser = tk.Button(self.marco_create, text="Crear\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.crear_usuario(permisos))
        self.buttonCreateUser.place(x=140, y=50)
        self.buttonEditUser = tk.Button(self.marco_create, text="Editar\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)
        self.buttonEditUser.place(x=250, y=50)
        self.buttonDeleteUser = tk.Button(self.marco_create, text="Desactivar\n Usuario", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)
        self.buttonDeleteUser.place(x=350, y=50)
        self.buttonModPerm = tk.Button(self.marco_create, text="Modificar\n Permisos", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)
        self.buttonModPerm.place(x=470, y=50)
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_usuarios = customtkinter.CTkLabel(self.marco_create, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_usuarios.place(x=140, y=155)

        self.sventrysearch_usuarios = customtkinter.StringVar()
        self.entrysearch_usuarios = ttk.Entry(self.marco_create, textvariable=self.sventrysearch_usuarios, style='Modern.TEntry', width=30)
        self.entrysearch_usuarios.place(x=175, y=157)
        self.entrysearch_usuarios.bind('<KeyRelease>', self.update_client_content)
        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.ListaUsuarios = consulUsers(where)
        else:
            self.ListaUsuarios = listarUsuarios()
            self.ListaUsuarios.reverse()

        self.tablaUsuarios = ttk.Treeview(self.marco_create, column=('coduser','username','password','idrol','data_create','data_update'), height=25)
        self.tablaUsuarios.place(x=145, y=200)

        #self.scroll = ttk.Scrollbar(self.marco_create, orient='vertical', command=self.tablaUsuarios.yview)
        #self.scroll.place(x=932, y=200, height=526)
        #self.tablaUsuarios.configure(yscrollcommand=self.scroll.set)
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
        self.tablaUsuarios.column("#4", width=125,stretch=False)
        self.tablaUsuarios.column("#5", width=125, stretch=False)
        self.tablaUsuarios.column("#6", width=125, stretch=False)

        
        #self.tablaUsuarios.bind('<Double-1>', self.crear_usuario)
        for p in self.ListaUsuarios:
            self.tablaUsuarios.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))
        
        self.tablaUsuarios.bind('<Double-1>', lambda event: self.crear_usuario(event, self.tablaUsuarios.item(self.tablaUsuarios.selection())['values']))

    def update_client_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_usuarios.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM usuarios WHERE
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
        for p in self.ListaUsuarios:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaUsuarios.delete(*self.tablaUsuarios.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaUsuarios.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        self.cursor.close()
        self.connection.close()

    def crear_usuario(self, permisos, values):
        #Creacion del top level
        topCreate = customtkinter.CTkToplevel()
        topCreate.title("Crear Usuarios")
        topCreate.iconbitmap("imagenes/logo_ico.ico") 
        topCreate.w = 600
        topCreate.h = 400
        topCreate.geometry(f"{topCreate.w}x{topCreate.h}")
        topCreate.resizable(False, False)
        
        #Centrar la ventana en la pantalla
        screen_width = topCreate.winfo_screenwidth()
        screen_height = topCreate.winfo_screenheight()
        x = (screen_width - topCreate.w) // 2
        y = (screen_height - topCreate.h) // 2
        topCreate.geometry(f"+{x}+{y}")

        
        topCreate.lift()
        topCreate.grab_set()
        topCreate.transient()

        selected_item = self.tablaUsuarios.focus()
        values = self.tablaUsuarios.item(selected_item)['values']
        #Datos para el usuario

        marco_crearusuario = customtkinter.CTkFrame(topCreate, width=550,height=350, bg_color="white", fg_color="white")
        marco_crearusuario.place(relx=0.5, rely=0.5, anchor="center")

        self.lblinfo = customtkinter.CTkLabel(marco_crearusuario, text="Creacion de nuevo usuario", font=("Roboto",14))
        self.lblinfo.place(x=205, rely=0.1)

        self.lblusuario = customtkinter.CTkLabel(marco_crearusuario, text='Username:', font=("Roboto", 14))
        self.lblusuario.place(x=50, y=120)

        self.svusuario = customtkinter.StringVar()
        self.entryusuario = ttk.Entry(marco_crearusuario, style='Modern.TEntry', textvariable=self.svusuario)
        self.entryusuario.place(x=125, y=120)
        self.entryusuario.configure(style='Entry.TEntry')

        #Datos de la Contraseña
        self.lblpassword = customtkinter.CTkLabel(marco_crearusuario, text='Password:', font=("Roboto", 14))
        self.lblpassword.place(x=50, y=170)
        
        self.svpassword = customtkinter.StringVar()
        self.entrypassword = ttk.Entry(marco_crearusuario, style='Modern.TEntry', textvariable=self.svpassword, show='*')
        self.entrypassword.place(x=125, y=170)
        self.entrypassword.configure(style='Entry.TEntry')

        roles = self.ObtenerRoles()
        self.svperfil_var = customtkinter.StringVar(value="Selecciona un perfil")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearusuario, values=roles, variable=self.svperfil_var)
        self.multioption.place(x=325, y=120)

        self.buttonCreate = customtkinter.CTkButton(marco_crearusuario, text="Crear Usuario", font=("Roboto", 12), command=self.GuardarUsuario)
        self.buttonCreate.place(x=215, y=250)

    def ObtenerRoles(self):
        try:
            
            self.connection = sqlite3.connect('database/database.db')
            self.cursor = self.connection.cursor()
    # Ob    tener el contenido del Entry
            self.content = self.entrysearch_usuarios.get()
    # Re    alizar la consulta
            self.cursor.execute("""SELECT id, name FROM roles""")
            self.resultado = self.cursor.fetchall()
            roles = []
            for resultado in self.resultado:
                roles.append(resultado[0])

            ids = [resultado[0] for resultado in self.resultado]
            nombres = [resultado[1] for resultado in self.resultado]

            return nombres
        except:
            pass
    def GuardarUsuario(self):
        try:
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
            
            usuario = usuarios(
                self.svusuario.get(),
                self.svpassword.get(),
                self.svperfil_var.get(),
                date_created,
                date_update
            )
            if self.id is None:
                SaveUser(usuario)
            else:
                EditUser(usuario, self.id)
            
            listarUsuarios()
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarUsuario, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')