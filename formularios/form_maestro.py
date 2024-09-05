import tkinter as tk
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
import customtkinter
import ctypes
from tkinter import font, ttk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_FONDO, COLOR_MENU_CURSOR_ENCIMA, COLOR_SUBMENU_LATERAL, COLOR_SUBMENU_CURSOR_ENCIMA, ANCHO_MENU, MITAD_MENU, ALTO_MENU, WIDTH_LOGO, HEIGHT_LOGO
from PIL import Image, ImageTk, ImageColor
from util.util_alerts import edit_advice, error_advice, save_advice, delete_advice, login_correct_advice, login_wrong_advice
from customtkinter import *
from ctypes import windll
from functions.conexion import ConexionDB
from tkinter import messagebox

from formularios.form_home import FormularioHomeDesign
from formularios.form_clients import FormClient
from formularios.form_users import FormUsers
from formularios.form_modulos import FormModulos
from formularios.form_permisos import FormPermisos
from formularios.form_perfiles import FormPerfiles
from formularios.form_proveedores import FormProv
from formularios.form_deposito import FormDepot
from formularios.form_products import FormProducts
from formularios.form_category import FormCategoria


class FormularioMaestro(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_cuerpo()
    def controles_cuerpo(self):    
        self.seccion_login()
        self.barra_superior.pack_forget()
        self.menu_lateral.pack_forget()
    def config_window(self):
        # Configuración inicial de la ventana
        self.bg = util_img.leer_imagen("./imagenes/background.png", (1440, 900))
        self.title("H.A.S.T - Herramienta Administrativa para Soporte Tecnico")
        self.set_window_icon()

        #self.geometry(f"{self.w}x{self.h}")
        self.resizable(False, False)
        self.iconbitmap("./imagenes/icons/logo_ico.ico")
        #util_ventana.centrar_ventana(self, self.w, self.h)
    def paneles(self):        
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 

        self.cuerpo_principal = tk.Frame(self)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    def set_window_icon(self):
        icon_path = "imagenes/icons/logo_ico.ico"  # Ruta del archivo de icono
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("HAST")  # Cambia "myappid" por un identificador único para tu aplicación
        self.iconbitmap(icon_path)
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = customtkinter.CTkFont(family='Roboto', size=12)
        # Etiqueta de título
        self.labelTitulo = customtkinter.CTkLabel(self.barra_superior, text="Menu", font=font_awesome,padx=20, text_color="white")
        self.labelTitulo.configure(fg_color="transparent", font=("Roboto", 15), bg_color='transparent', pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)
        self.menu_original_image = Image.open("imagenes/icons/menu.png")
        self.menu_resized_image = self.menu_original_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.menu_image = ImageTk.PhotoImage(self.menu_resized_image)
        # Botón del menú lateral
        self.buttonMenuLateral = customtkinter.CTkButton(self.barra_superior, text="", image=self.menu_image,
                                        command=self.toggle_panel, bg_color='transparent', fg_color='transparent', hover=False, width=WIDTH_LOGO, height=HEIGHT_LOGO)
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=20)
    def controles_menu_lateral(self, permisos):
        self.logo = util_img.leer_imagen("./imagenes/icons/logo.png", (100, 100))
        ## ESTO AUN NO ESTA DEFINIDO
        self.labellogo = tk.Label(self.menu_lateral, image=self.logo, bg=COLOR_MENU_LATERAL)
        self.labellogo.pack(side=tk.TOP, pady=15, padx=10)
        
        #RUTAS DE LAS IMAGENES
        home_image = Image.open("imagenes/icons/home.png")
        #Home Resized
        home_resized = home_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #Home Finals
        self.home_icon = ImageTk.PhotoImage(home_resized)

        #Proveedores 
        prov_image = Image.open("imagenes/icons/prov.png")
        listProv_image = Image.open("imagenes/icons/listprov.png")
        #Prov Resized
        prov_resized = prov_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        listProv_resized = listProv_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #Prov Final
        self.prov_icon = ImageTk.PhotoImage(prov_resized)
        self.listProv_icon = ImageTk.PhotoImage(listProv_resized)

        #Clients
        client_image = Image.open("imagenes/icons/clients.png")
        regClient_image = Image.open("imagenes/icons/addclient.png")
        #Clients Resized
        client_resized = client_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        regClient_resized = regClient_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #Clients Final
        self.client_icon = ImageTk.PhotoImage(client_resized)
        self.regClient_icon = ImageTk.PhotoImage(regClient_resized)

        #Settings
        settings_image = Image.open("imagenes/icons/settings.png")
        adjustUser_image = Image.open("imagenes/icons/user_adjust.png")
        userProfiles_image = Image.open("imagenes/icons/user_profiles.png") 
        permises_image = Image.open("imagenes/icons/permise.png")
        adjustModul_image = Image.open("imagenes/icons/module.png")
        #Settings Resized
        settings_resized = settings_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        adjustUser_resized = adjustUser_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        userProfiles_resized = userProfiles_image.resize((WIDTH_LOGO, HEIGHT_LOGO)) 
        permises_resized = permises_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        adjustModul_resized = adjustModul_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #Settings Finals
        self.settings_icon = ImageTk.PhotoImage(settings_resized)
        self.adjustUser_icon = ImageTk.PhotoImage(adjustUser_resized)
        self.userProfiles_icon = ImageTk.PhotoImage(userProfiles_resized)
        self.permises_icon = ImageTk.PhotoImage(permises_resized)
        self.adjustModul_icon = ImageTk.PhotoImage(adjustModul_resized)
        
        #Products
        products_image = Image.open("imagenes/icons/product.png")
        category_image = Image.open("imagenes/icons/product_cat.png")
        #Products Resized
        products_resized = products_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        category_resized = category_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #Products Finals
        self.products_icon = ImageTk.PhotoImage(products_resized)
        self.category_icon = ImageTk.PhotoImage(category_resized)

        #Almacen
        almacen_image = Image.open("imagenes/icons/almacen.png")
        adjustdepot_image = Image.open("imagenes/icons/adjustdepot.png")
        #Almacen Resized
        almacen_resized = almacen_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        adjustdepot_resized = adjustdepot_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #Almacen Finals
        self.adjustdepot_icon = ImageTk.PhotoImage(adjustdepot_resized)
        self.almacen_icon = ImageTk.PhotoImage(almacen_resized)

        #BOTONES DEL MENU
        #Home1001 visualizar modulo home
        if 'HOME1001' in permisos:
            self.buttonHome = tk.Button(self.menu_lateral, text="Inicio", font=("Roboto", 16), image=self.home_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.abrir_home)
            self.buttonHome.pack()
            self.binding_hover_event(self.buttonHome)
        else:
            pass
        if 'ALMA1001' in permisos:
            self.buttonAlmacen = tk.Button(self.menu_lateral, text="Almacen",  font=("Roboto", 16), image=self.almacen_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenu_almacen(permisos))
            self.buttonAlmacen.pack()
            self.binding_hover_event(self.buttonAlmacen)
        else:
            pass

        if 'PROV1001' in permisos:
            self.buttonProveedores = tk.Button(self.menu_lateral, text="Proveedores", font=("Roboto", 16), image=self.prov_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenu_proveedores(permisos))
            self.buttonProveedores.pack()
            self.binding_hover_event(self.buttonProveedores) 
        else:
            pass

        if 'CLIE1001' in permisos:
            self.buttonClient = tk.Button(self.menu_lateral, text="Clientes",  font=("Roboto", 16),  image=self.client_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenu_clientes(permisos))        
            self.buttonClient.pack()
            self.binding_hover_event(self.buttonClient)
        else:
            pass

        if 'CONF1001' in permisos:
            self.buttonSettings = tk.Button(self.menu_lateral, text="Ajustes",  font=("Roboto", 16),image=self.settings_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenu_config(permisos))
            self.buttonSettings.pack()
            self.binding_hover_event(self.buttonSettings)
        else:
            pass
    def seccion_login(self):
        self.w, self.h = 800, 600
        self.geometry(f"{self.w}x{self.h}")
        util_ventana.centrar_ventana(self, self.w, self.h)
        ############# INICIALIZACION DE LA IMAGEN DE FONDO AUTOEXPANDIBLE #############
        ruta_imagen = "imagenes/bg.png"
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_tk = imagen_tk
        # Crear el Label con la imagen de fondo
        label_fondo = tk.Label(self.cuerpo_principal, image=imagen_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_fondo = label_fondo
        # Configurar el Label para que se ajuste automáticamente al tamaño del frame
        def ajustar_imagen(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
        
        self.cuerpo_principal.bind("<Configure>", ajustar_imagen)

        def validarDatos():
            conexion = ConexionDB()
            
            username = sv_datauser.get()
            password = sv_datapass.get()

            sql = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
            conexion.ejecutar_consulta(sql)
            resultado = conexion.obtener_resultado()
            

            if resultado:

                usuario = resultado[2]
                contrasena = resultado[3]
                idrol = resultado[4]
                activo = resultado[7]

                login_correct_advice()

                datauser = {
                    'username': usuario,
                    'password': contrasena,
                    'idrol': idrol,
                    'activo': activo
                } 

                self.obtener_idrol(idrol)
                self.barra_superior.pack(side=tk.TOP, fill='both')
                self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
                self.cuerpo_principal.destroy()
                self.cuerpo_principal = tk.Frame(self)
                self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
                self.w, self.h = 1440, 900
                self.geometry(f"{self.w}x{self.h}")
                self.resizable(True, True)
                util_ventana.centrar_ventana(self, self.w, self.h)
                self.abrir_home()
            else:
                login_wrong_advice()

        def set_opacity(widget, value: float):
            widget = widget.winfo_id()
            value = int(255*value) # value from 0 to 1
            wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
            new_exstyle = wnd_exstyle | 0x00080000  
            windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
            windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)

        marco_login = customtkinter.CTkFrame(self.cuerpo_principal, fg_color="white", width=300, height=250)
        marco_login.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(marco_login, 0.9)
        #Iconos
        user_ico = Image.open("imagenes/icons/user.png")
        user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        user_img = ImageTk.PhotoImage(user_ico)

        pass_ico = Image.open("imagenes/icons/pass.png")
        pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        pass_img = ImageTk.PhotoImage(pass_ico)

        #LOGIN USER
        lbluser = customtkinter.CTkLabel(marco_login, text="", image=user_img, bg_color="white")
        lbluser.pack(pady=1, padx=6)
        lbluser.place(x=55, y=55)
        
        set_opacity(lbluser, 0.8)

        sv_datauser = customtkinter.StringVar()
        style = ttk.Style()
        style.configure("Custom.TEntry", borderwidth=0)

        entryuser = ttk.Entry(marco_login, textvariable=sv_datauser, width=14, font=("Arial", 12), style="Custom.TEntry", justify="center")
        entryuser.place(x=105, y=56)
        #LOGIN PASSWORD
        lblpass = customtkinter.CTkLabel(marco_login, text="", image=pass_img, bg_color="white")
        lblpass.pack(pady=1, padx=6)
        lblpass.place(x=55, y=125)

        set_opacity(lblpass, 0.8)

        sv_datapass = customtkinter.StringVar()
        #entrypass = customtkinter.CTkEntry(self.cuerpo_principal, textvariable=sv_datapass, show="*", width=150)
        entrypass = ttk.Entry(marco_login, textvariable=sv_datapass, width=14, font=("Arial", 13), style="Custom.TEntry", show="*", justify="center")
        entrypass.place(x=105, y=126)
        entrypass.bind("<Return>", lambda event: validarDatos())
        
        #LOGIN BOTON
        stylebutton = ttk.Style()
        stylebutton.configure("Custom.TButton")
        btnLogIn = ttk.Button(marco_login, text="Iniciar Sesion", command=validarDatos, width=14, style="Custom.TButton")
        btnLogIn.place(x=120, y=180)
    def obtener_idrol(self, idrol):
        self
        conexion = ConexionDB()
        sql = f"SELECT codpermiso FROM asigperm WHERE idrol = '{idrol}'"
        conexion.ejecutar_consulta(sql)
        resultados = conexion.obtener_resultados()
        permisos = []
        for resultado in resultados:
            permisos.append(resultado[0])

        self.permisos_actualizados = permisos
        if permisos:
            #self.prueba_menu_lateral(permisos)
            self.controles_menu_lateral(permisos)
        else:
            return None
    def submenu_almacen(self, permisos):
        #LIMPIEZA PROVEEDORES
        if 'PROV1001' in permisos:
            self.buttonProveedores.pack_forget()
        if 'PROV1002' in permisos:
            if hasattr(self, "buttonListaProv"):
                self.buttonListaProv.pack_forget()
                del self.buttonListaProv
        #LIMPIEZA EN CLIENTES
        if 'CLIE1001' in permisos:
            self.buttonClient.pack_forget()
        #LIMPIEZA CLIENTES
        if 'CLIE1002' in permisos:
            if hasattr(self, "buttonRegClient"):
                self.buttonRegClient.pack_forget()
                del self.buttonRegClient
        #LIMPIEZA EN AJUSTES
        if 'CONF1001' in permisos:
            self.buttonSettings.pack_forget()
        if 'CONF1002' in permisos:
            if hasattr(self, "buttonAdjustUsers"):
                self.buttonAdjustUsers.pack_forget()
                del self.buttonAdjustUsers
        if 'CONF1003' in permisos:
            if hasattr(self, "buttonAdjustProfiles"):
                self.buttonAdjustProfiles.pack_forget()
                del self.buttonAdjustProfiles
        if 'CONF1004' in permisos:
            if hasattr(self, "buttonModulos"):
                self.buttonModulos.pack_forget()
                del self.buttonModulos
        if 'CONF1005' in permisos:
            if hasattr(self, "buttonPermisos"):
                self.buttonPermisos.pack_forget()
                del self.buttonPermisos
        #INICIALIZACION SUBMENU ALMACEN
        if 'ALMA1002' in permisos:  
            if hasattr(self, "buttonDepositos"):
                self.buttonDepositos.pack_forget()
                del self.buttonDepositos
            else:
                self.buttonDepositos = tk.Button(self.menu_lateral, text="Depositos", font=("Roboto", 12), image=self.adjustdepot_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_Depots(permisos))
                self.buttonDepositos.pack()
                self.binding_hover_submenu_event(self.buttonDepositos)
        if 'ALMA1003' in permisos:
            if hasattr(self, "buttonProductos"):
                self.buttonProductos.pack_forget()
                del self.buttonProductos
            else:
                self.buttonProductos = tk.Button(self.menu_lateral, text="Productos", font=("Roboto", 12),image=self.products_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_Productos(permisos))
                self.buttonProductos.pack()
                self.binding_hover_submenu_event(self.buttonProductos)
        if 'ALMA1004' in permisos:
            if hasattr(self, "buttonCatArt"):
                self.buttonCatArt.pack_forget()
                del self.buttonCatArt
            else:
                self.buttonCatArt = tk.Button(self.menu_lateral, text="Categoria de\nProductos", font=("Roboto", 12),image=self.category_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_categoria(permisos))
                
                self.buttonCatArt.pack()
                self.binding_hover_submenu_event(self.buttonCatArt)
        if 'PROV1001' in permisos:
            self.buttonProveedores.pack()
        if 'CLIE1001' in permisos:
            self.buttonClient.pack()
        if 'CONF1001' in permisos:
            self.buttonSettings.pack()
    def submenu_proveedores(self, permisos):
        #VERIFICAR LOS PERMISOS Y QUE BOTONES ESTAN DISPONIBLES  
        #LIMPIEZA DE ALMACEN Y SUBMENU      
        if 'ALMA1002' in permisos:
            if hasattr(self, "buttonDepositos"):
                self.buttonDepositos.pack_forget()
                del self.buttonDepositos
        if 'ALMA1003' in permisos:
            if hasattr(self, "buttonProductos"):
                self.buttonProductos.pack_forget()
                del self.buttonProductos
        if 'ALMA1004' in permisos:
            if hasattr(self, "buttonCatArt"):
                self.buttonCatArt.pack_forget()
                del self.buttonCatArt
        #LIMPIEZA EN CLIENTES
        if 'CLIE1001' in permisos:
            self.buttonClient.pack_forget()
        #LIMPIEZA CLIENTES
        if 'CLIE1002' in permisos:
            if hasattr(self, "buttonRegClient"):
                self.buttonRegClient.pack_forget()
                del self.buttonRegClient
        #LIMPIEZA DE AJUSTES Y SUBMENU
        if 'CONF1001' in permisos:
            if hasattr(self, "buttonSettings"):
                self.buttonSettings.pack_forget()
        if 'CONF1002' in permisos:
            if hasattr(self, "buttonAdjustUsers"):
                self.buttonAdjustUsers.pack_forget()
                del self.buttonAdjustUsers
        if 'CONF1003' in permisos:
            if hasattr(self, "buttonAdjustProfiles"):
                self.buttonAdjustProfiles.pack_forget()
                del self.buttonAdjustProfiles
        if 'CONF1004' in permisos:
            if hasattr(self, "buttonModulos"):
                self.buttonModulos.pack_forget()
                del self.buttonModulos
        if 'CONF1005' in permisos:
            if hasattr(self, "buttonPermisos"):
                self.buttonPermisos.pack_forget()
                del self.buttonPermisos
        #INICIALIZACION DE PROVEEDORES
        if 'ALMA1001' in permisos:
            self.buttonAlmacen.pack()
        
        if 'PROV1002' in permisos:
            if hasattr(self, "buttonListaProv"):
                self.buttonListaProv.pack_forget()
                del self.buttonListaProv
            else:
                self.buttonListaProv = tk.Button(self.menu_lateral, text="Listado de\n Proveedores", font=("Roboto", 12), image=self.listProv_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_proveedores(permisos))
                self.buttonListaProv.pack()
                self.binding_hover_submenu_event(self.buttonListaProv)
        
            pass
        #INICIALIZACION CLIENTES
        if 'CLIE1001' in permisos:
            self.buttonClient.pack()
        #INICIALIZACION AJUSTES
        if 'CONF1001' in permisos:
            self.buttonSettings.pack()
        else:
            pass   
    def submenu_config(self, permisos):
        #lIMPIEZA DE SUBMENU ALMACEN
        if 'ALMA1002' in permisos:
            if hasattr(self, "buttonDepositos"):
                self.buttonDepositos.pack_forget()
                del self.buttonDepositos
        if 'ALMA1003' in permisos:
            if hasattr(self, "buttonProductos"):
                self.buttonProductos.pack_forget()
                del self.buttonProductos
        if 'ALMA1004' in permisos:
            if hasattr(self, "buttonCatArt"):
                self.buttonCatArt.pack_forget()
                del self.buttonCatArt
        #LIMPIEZA SUBMENU PROVEEDORES
        if 'PROV1002' in permisos:
            if hasattr(self, "buttonListaProv"):
                self.buttonListaProv.pack_forget()
                del self.buttonListaProv
        #LIMPIEZA CLIENTES
        if 'CLIE1002' in permisos:
            if hasattr(self, "buttonRegClient"):
                self.buttonRegClient.pack_forget()
                del self.buttonRegClient
        #INICIALIZACION DE CLIENTES
        if 'CLIE1001' in permisos:
            self.buttonClient.pack()
        #INICIALIZACION DE SUBMENU DE AJUSTES
        if 'CONF1002' in permisos:
            if hasattr(self, "buttonAdjustUsers"):
                self.buttonAdjustUsers.pack_forget()
                del self.buttonAdjustUsers
            else:
                self.buttonAdjustUsers = tk.Button(self.menu_lateral, text="Ajuste de Usuario", font=("Roboto", 12), image=self.adjustUser_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_usuarios(permisos))
                self.buttonAdjustUsers.pack()

                self.binding_hover_submenu_event(self.buttonAdjustUsers)
        if 'CONF1003' in permisos:
            if hasattr(self, "buttonAdjustProfiles"):
                self.buttonAdjustProfiles.pack_forget()
                del self.buttonAdjustProfiles
            else:
                self.buttonAdjustProfiles = tk.Button(self.menu_lateral, text="Ajuste de Perfiles", font=("Roboto", 12), image=self.userProfiles_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_adjustProfile(permisos))
                self.buttonAdjustProfiles.pack()

                self.binding_hover_submenu_event(self.buttonAdjustProfiles)
        if 'CONF1004' in permisos:
            if hasattr(self, "buttonModulos"):
                self.buttonModulos.pack_forget()
                del self.buttonModulos
            else:
                self.buttonModulos = tk.Button(self.menu_lateral, text="Ajuste de Modulo", font=("Roboto", 12), image=self.adjustModul_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_modulos(permisos))
                self.buttonModulos.pack()

                self.binding_hover_submenu_event(self.buttonModulos)

        if 'CONF1005' in permisos:
            if hasattr(self, "buttonPermisos"):
                self.buttonPermisos.pack_forget()
                del self.buttonPermisos
            else:
                self.buttonPermisos = tk.Button(self.menu_lateral, text="Permisos", font=("Roboto", 12), image=self.permises_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_permisos(permisos))
                self.buttonPermisos.pack()
            
                self.binding_hover_submenu_event(self.buttonPermisos)
    def submenu_clientes(self, permisos):
        #lIMPIEZA DE SUBMENU ALMACEN
        if 'ALMA1002' in permisos:
            if hasattr(self, "buttonDepositos"):
                self.buttonDepositos.pack_forget()
                del self.buttonDepositos
        if 'ALMA1003' in permisos:
            if hasattr(self, "buttonProductos"):
                self.buttonProductos.pack_forget()
                del self.buttonProductos
        if 'ALMA1004' in permisos:
            if hasattr(self, "buttonCatArt"):
                self.buttonCatArt.pack_forget()
                del self.buttonCatArt
        #LIMPIEZA SUBMENU PROVEEDORES
        if 'PROV1002' in permisos:
            if hasattr(self, "buttonListaProv"):
                self.buttonListaProv.pack_forget()
                del self.buttonListaProv
        #LIMPIEZA DE AJUSTES Y SUBMENU
        if 'CONF1001' in permisos:
            if hasattr(self, "buttonSettings"):
                self.buttonSettings.pack_forget()
        if 'CONF1002' in permisos:
            if hasattr(self, "buttonAdjustUsers"):
                self.buttonAdjustUsers.pack_forget()
                del self.buttonAdjustUsers
        if 'CONF1003' in permisos:
            if hasattr(self, "buttonAdjustProfiles"):
                self.buttonAdjustProfiles.pack_forget()
                del self.buttonAdjustProfiles
        if 'CONF1004' in permisos:
            if hasattr(self, "buttonModulos"):
                self.buttonModulos.pack_forget()
                del self.buttonModulos
        if 'CONF1005' in permisos:
            if hasattr(self, "buttonPermisos"):
                self.buttonPermisos.pack_forget()
                del self.buttonPermisos

        #INICIALIZACION CLIENTES
        if 'CLIE1002' in permisos:
            if hasattr(self, "buttonRegClient"):
                self.buttonRegClient.pack_forget()
                del self.buttonRegClient
            else:
                self.buttonRegClient = tk.Button(self.menu_lateral, text="Registro\nde Clientes",  font=("Roboto", 15), image=self.regClient_icon, highlightthickness=20, width=ANCHO_MENU,
                    height=ALTO_MENU, bg=COLOR_SUBMENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_regclientes(permisos))        
                self.buttonRegClient.pack()

                self.binding_hover_submenu_event(self.buttonRegClient)

        #INICIALIZACION CONFIG
        if 'CONF1001' in permisos:
            self.buttonSettings.pack()
    def obtener_idrol(self, idrol):
        conexion = ConexionDB()
        sql = f"SELECT codpermiso FROM asigperm WHERE idrol = '{idrol}'"
        conexion.ejecutar_consulta(sql)
        resultados = conexion.obtener_resultados()
        permisos = []
        for resultado in resultados:
            permisos.append(resultado[0])
        
        self.permisos_actualizados = permisos

        if permisos:
            #self.prueba_menu_lateral(permisos)
            self.controles_menu_lateral(permisos)
        else:
            return None
    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
    def check_size(self):
        width_screen = self.winfo_width()
        height_screen = self.winfo_height()
    
        return width_screen, height_screen
    
    #def abrir_registros_clientes(self):
    #    self.limpiar_panel(self.cuerpo_principal)
    #    width_screen, height_screen = self.check_size()
    #    if width_screen > 1440 and height_screen > 900:
    #        FormularioRegistrosDesign(self.cuerpo_principal, width_screen, height_screen).call_resize(width_screen, height_screen)
    #    elif width_screen <= 1440 and height_screen <= 900:
    #        FormularioRegistrosDesign(self.cuerpo_principal,width_screen, height_screen)

    def abrir_usuarios(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormUsers(self.cuerpo_principal, permisos) 
    def abrir_proveedores(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormProv(self.cuerpo_principal, permisos)
    def abrir_regclientes(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormClient(self.cuerpo_principal, permisos)       
    def abrir_modulos(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormModulos(self.cuerpo_principal, permisos)
    def abrir_permisos(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormPermisos(self.cuerpo_principal, permisos)
    def abrir_categoria(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormCategoria(self.cuerpo_principal, permisos)
    def abrir_home(self):   
        self.limpiar_panel(self.cuerpo_principal)
        FormularioHomeDesign(self.cuerpo_principal) 
    def abrir_adjustProfile(self, permisos):   
        self.limpiar_panel(self.cuerpo_principal)
        FormPerfiles(self.cuerpo_principal, permisos)
    def abrir_Depots(self, permisos):   
        self.limpiar_panel(self.cuerpo_principal)
        FormDepot(self.cuerpo_principal, permisos)
    def abrir_Productos(self, permisos):   
        self.limpiar_panel(self.cuerpo_principal)
        FormProducts(self.cuerpo_principal, permisos)

    def limpiar_panel(self, panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()
    def binding_hover_event(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white', anchor="w")

    def on_leave(self, event, button):
        button.config(bg=COLOR_MENU_LATERAL, fg='white', anchor="w")

    def binding_hover_submenu_event(self, button):
        button.bind("<Enter>", lambda event: self.submenu_on_enter(event, button))
        button.bind("<Leave>", lambda event: self.submenu_on_leave(event, button))

    def submenu_on_enter(self, event, button):
        button.config(bg=COLOR_SUBMENU_CURSOR_ENCIMA, fg='white', anchor="w", height=ALTO_MENU)

    def submenu_on_leave(self, event, button):
        button.config(bg=COLOR_SUBMENU_LATERAL, fg='white', anchor="w", height=MITAD_MENU)