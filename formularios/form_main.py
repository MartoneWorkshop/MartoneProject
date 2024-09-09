import tkinter as tk
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
import customtkinter
from tkinter import font, ttk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_FONDO, COLOR_MENU_CURSOR_ENCIMA, COLOR_SUBMENU_LATERAL, COLOR_SUBMENU_CURSOR_ENCIMA, ANCHO_MENU, MITAD_MENU, ALTO_MENU, WIDTH_LOGO, HEIGHT_LOGO
from PIL import Image, ImageTk, ImageColor
from util.util_alerts import edit_advice, error_advice, save_advice, delete_advice, login_correct_advice, login_wrong_advice
from customtkinter import *
from functions.conexion import ConexionDB
from tkinter import messagebox

from formularios.form_dashboard import formDashboard
from formularios.form_clients import FormClient
from formularios.form_users import FormUsers
from formularios.form_modules import FormModules
from formularios.form_permiss import FormPermissions
from formularios.form_profiles import FormProfiles
from formularios.form_suppliers import FormSuppliers
from formularios.form_depots import FormDepot
from formularios.form_products import FormProducts
from formularios.form_category import FormCategory
from util.util_ventana import set_window_icon, set_opacity, binding_hover_event, binding_hover_submenu_event, cleanPanel

class FormMain(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.createPanels()
        self.topBarControls()
        self.bodyControls()
    def bodyControls(self):    
        self.loginSection()
        self.barra_superior.pack_forget()
        self.menu_lateral.pack_forget()
    def config_window(self):
        # Configuración inicial de la ventana
        self.bg = util_img.leer_imagen("./imagenes/background.png", (1440, 900))
        self.title("H.A.S.T - Herramienta Administrativa para Soporte Tecnico")
        set_window_icon(self)

        #self.geometry(f"{self.w}x{self.h}")
        self.resizable(False, False)
        self.iconbitmap("./imagenes/icons/logo_ico.ico")
        #util_ventana.centrar_ventana(self, self.w, self.h)
    def createPanels(self):        
        # Crear createPanels:
        #Barra Superior
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')
        #Menu Lateral
        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        #Cuerpo Principal
        self.cuerpo_principal = tk.Frame(self)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    def topBarControls(self):
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
    def menuControls(self, permisos):
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
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.openFormDashboard)
            self.buttonHome.pack()
            binding_hover_event(self.buttonHome)
        else:
            pass
        if 'ALMA1001' in permisos:
            self.buttonAlmacen = tk.Button(self.menu_lateral, text="Almacen",  font=("Roboto", 16), image=self.almacen_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenuStore(permisos))
            self.buttonAlmacen.pack()
            binding_hover_event(self.buttonAlmacen)
        else:
            pass

        if 'PROV1001' in permisos:
            self.buttonProveedores = tk.Button(self.menu_lateral, text="Proveedores", font=("Roboto", 16), image=self.prov_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenuSuppliers(permisos))
            self.buttonProveedores.pack()
            binding_hover_event(self.buttonProveedores) 
        else:
            pass

        if 'CLIE1001' in permisos:
            self.buttonClient = tk.Button(self.menu_lateral, text="Clientes",  font=("Roboto", 16),  image=self.client_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenuClients(permisos))        
            self.buttonClient.pack()
            binding_hover_event(self.buttonClient)
        else:
            pass

        if 'CONF1001' in permisos:
            self.buttonSettings = tk.Button(self.menu_lateral, text="Ajustes",  font=("Roboto", 16),image=self.settings_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenuConfig(permisos))
            self.buttonSettings.pack()
            binding_hover_event(self.buttonSettings)
        else:
            pass
    def loginSection(self):
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
        def adjustImage(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
        
        self.cuerpo_principal.bind("<Configure>", adjustImage)

        def validateLogin():
            conexion = ConexionDB()
            
            username = sv_datauser.get()
            password = sv_datapass.get()

            sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
            conexion.execute_consult(sql)
            resultado = conexion.get_result()
            

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

                self.get_idrol(idrol)
                self.barra_superior.pack(side=tk.TOP, fill='both')
                self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
                self.cuerpo_principal.destroy()
                self.cuerpo_principal = tk.Frame(self)
                self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
                self.w, self.h = 1440, 900
                self.geometry(f"{self.w}x{self.h}")
                self.resizable(True, True)
                util_ventana.centrar_ventana(self, self.w, self.h)
                self.openFormDashboard()
            else:
                login_wrong_advice()

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
        entrypass.bind("<Return>", lambda event: validateLogin())
        
        #LOGIN BOTON
        stylebutton = ttk.Style()
        stylebutton.configure("Custom.TButton")
        btnLogIn = ttk.Button(marco_login, text="Iniciar Sesion", command=validateLogin, width=14, style="Custom.TButton")
        btnLogIn.place(x=120, y=180)
    def get_idrol(self, idrol):
        self
        conexion = ConexionDB()
        sql = f"SELECT codpermiso FROM asigperm WHERE idrol = '{idrol}'"
        conexion.execute_consult(sql)
        resultados = conexion.get_results()
        permisos = []
        for resultado in resultados:
            permisos.append(resultado[0])

        self.permisos_actualizados = permisos
        if permisos:
            #self.prueba_menu_lateral(permisos)
            self.menuControls(permisos)
        else:
            return None
    def submenuStore(self, permisos):
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
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormDepots(permisos))
                self.buttonDepositos.pack()
                binding_hover_submenu_event(self.buttonDepositos)
        if 'ALMA1003' in permisos:
            if hasattr(self, "buttonProductos"):
                self.buttonProductos.pack_forget()
                del self.buttonProductos
            else:
                self.buttonProductos = tk.Button(self.menu_lateral, text="Productos", font=("Roboto", 12),image=self.products_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormProducts(permisos))
                self.buttonProductos.pack()
                binding_hover_submenu_event(self.buttonProductos)
        if 'ALMA1004' in permisos:
            if hasattr(self, "buttonCatArt"):
                self.buttonCatArt.pack_forget()
                del self.buttonCatArt
            else:
                self.buttonCatArt = tk.Button(self.menu_lateral, text="Categoria de\nProductos", font=("Roboto", 12),image=self.category_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormCategory(permisos))
                
                self.buttonCatArt.pack()
                binding_hover_submenu_event(self.buttonCatArt)
        if 'PROV1001' in permisos:
            self.buttonProveedores.pack()
        if 'CLIE1001' in permisos:
            self.buttonClient.pack()
        if 'CONF1001' in permisos:
            self.buttonSettings.pack()
    def submenuSuppliers(self, permisos):
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
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormSuppliers(permisos))
                self.buttonListaProv.pack()
                binding_hover_submenu_event(self.buttonListaProv)
        
            pass
        #INICIALIZACION CLIENTES
        if 'CLIE1001' in permisos:
            self.buttonClient.pack()
        #INICIALIZACION AJUSTES
        if 'CONF1001' in permisos:
            self.buttonSettings.pack()
        else:
            pass   
    def submenuConfig(self, permisos):
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
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormUser(permisos))
                self.buttonAdjustUsers.pack()

                binding_hover_submenu_event(self.buttonAdjustUsers)
        if 'CONF1003' in permisos:
            if hasattr(self, "buttonAdjustProfiles"):
                self.buttonAdjustProfiles.pack_forget()
                del self.buttonAdjustProfiles
            else:
                self.buttonAdjustProfiles = tk.Button(self.menu_lateral, text="Ajuste de Perfiles", font=("Roboto", 12), image=self.userProfiles_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormAdjustProfile(permisos))
                self.buttonAdjustProfiles.pack()

                binding_hover_submenu_event(self.buttonAdjustProfiles)
        if 'CONF1004' in permisos:
            if hasattr(self, "buttonModulos"):
                self.buttonModulos.pack_forget()
                del self.buttonModulos
            else:
                self.buttonModulos = tk.Button(self.menu_lateral, text="Ajuste de Modulo", font=("Roboto", 12), image=self.adjustModul_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormModules(permisos))
                self.buttonModulos.pack()

                binding_hover_submenu_event(self.buttonModulos)

        if 'CONF1005' in permisos:
            if hasattr(self, "buttonPermisos"):
                self.buttonPermisos.pack_forget()
                del self.buttonPermisos
            else:
                self.buttonPermisos = tk.Button(self.menu_lateral, text="Permisos", font=("Roboto", 12), image=self.permises_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormPermission(permisos))
                self.buttonPermisos.pack()
            
                binding_hover_submenu_event(self.buttonPermisos)
    def submenuClients(self, permisos):
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
                self.buttonRegClient = tk.Button(self.menu_lateral, text="Registro\nde Clientes",  font=("Roboto", 13), image=self.regClient_icon, highlightthickness=20, width=ANCHO_MENU,
                    height=ALTO_MENU, bg=COLOR_SUBMENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.openFormRegClient(permisos))        
                self.buttonRegClient.pack()

                binding_hover_submenu_event(self.buttonRegClient)

        #INICIALIZACION CONFIG
        if 'CONF1001' in permisos:
            self.buttonSettings.pack()
    def get_idrol(self, idrol):
        conexion = ConexionDB()
        sql = f"SELECT codpermiso FROM asigperm WHERE idrol = '{idrol}'"
        conexion.execute_consult(sql)
        resultados = conexion.get_results()
        permisos = []
        for resultado in resultados:
            permisos.append(resultado[0])
        
        self.permisos_actualizados = permisos

        if permisos:
            #self.prueba_menu_lateral(permisos)
            self.menuControls(permisos)
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
    def openFormUser(self, permisos):
        cleanPanel(self.cuerpo_principal)
        FormUsers(self.cuerpo_principal, permisos) 
    def openFormSuppliers(self, permisos):
        cleanPanel(self.cuerpo_principal)
        FormSuppliers(self.cuerpo_principal, permisos)
    def openFormRegClient(self, permisos):
        cleanPanel(self.cuerpo_principal)
        FormClient(self.cuerpo_principal, permisos)       
    def openFormModules(self, permisos):
        cleanPanel(self.cuerpo_principal)
        FormModules(self.cuerpo_principal, permisos)
    def openFormPermission(self, permisos):
        cleanPanel(self.cuerpo_principal)
        FormPermissions(self.cuerpo_principal, permisos)
    def openFormCategory(self, permisos):
        cleanPanel(self.cuerpo_principal)
        FormCategory(self.cuerpo_principal, permisos)
    def openFormDashboard(self):   
        cleanPanel(self.cuerpo_principal)
        formDashboard(self.cuerpo_principal) 
    def openFormAdjustProfile(self, permisos):   
        cleanPanel(self.cuerpo_principal)
        FormProfiles(self.cuerpo_principal, permisos)
    def openFormDepots(self, permisos):   
        cleanPanel(self.cuerpo_principal)
        FormDepot(self.cuerpo_principal, permisos)
    def openFormProducts(self, permisos):   
        cleanPanel(self.cuerpo_principal)
        FormProducts(self.cuerpo_principal, permisos)

