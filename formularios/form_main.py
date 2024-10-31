import tkinter as tk
import util.util_screen as util_screen
import util.util_imagenes as util_img
import platform
import customtkinter
from tkinter import font, ttk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_FONDO, COLOR_MENU_CURSOR_ENCIMA, COLOR_SUBMENU_LATERAL, COLOR_SUBMENU_CURSOR_ENCIMA, ANCHO_MENU, MITAD_MENU, ALTO_MENU, WIDTH_LOGO, HEIGHT_LOGO, WIDTH_LOGO_MAX, HEIGHT_LOGO_MAX
from PIL import Image, ImageTk, ImageColor
from util.util_alerts import set_opacity, edit_advice, error_advice, save_advice, delete_advice, login_correct_advice, login_wrong_advice
from customtkinter import *
from functions.conexion import ConexionDB
from tkinter import messagebox


from Revisar.form_dashboard import formDashboard
from formularios.form_clients import FormClient
from formularios.form_users import FormUsers
from formularios.form_modules import FormModules
from formularios.form_permiss import FormPermissions
from formularios.form_profiles import FormProfiles
from formularios.form_suppliers import FormSuppliers
from formularios.form_depots import FormDepot
from formularios.form_products import FormProducts
from formularios.form_category import FormCategory
from util.util_screen import set_window_icon, binding_hover_event, binding_hover_submenu_event_min, binding_hover_submenu_event, binding_hover_event_min, cleanPanel, loadBackgroundImage, centerWidget

class FormMain(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.createPanels()
        self.load_images()
        self.topBarControls()
        self.bodyControls()
        self.botones = []
        self.textos_originales = []
        self.submenu_frames = {}
        self.submenu_visible = False
        self.current_submenu_frame = None
    def bodyControls(self):    
        self.loginSection()
        self.barra_superior.pack_forget()
        self.menu_lateral.pack_forget()
    def config_window(self):
        # Configuración inicial de la ventana
        self.bg = util_img.leer_imagen("./imagenes/bg4.jpeg", (1440, 900))
        self.title("H.A.S.T - Herramienta Administrativa para Soporte Tecnico")
        set_window_icon(self)
        self.resizable(False, False)

        if platform.system() == "Windows":
            self.iconbitmap("./imagenes/icons/logo_ico.ico")
        else:
        # Carga el ícono en formato PNG para Linux
            self.icon = ImageTk.PhotoImage(file="./imagenes/icons/logo.png")
            self.tk.call('wm', 'iconphoto', self._w, self.icon)
    def createPanels(self):        
        # Crear createPanels:
        #Barra Superior
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X)
        #Menu Lateral
        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill=tk.Y)
        #Cuerpo Principal
        self.cuerpo_principal = tk.Frame(self)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    def load_images(self):
        # Define un diccionario para almacenar las imágenes
        self.images = {
            'logo': './imagenes/icons/logo.png',
            'home': 'imagenes/icons/home.png',
            'prov': 'imagenes/icons/prov.png',
            'listprov': 'imagenes/icons/listprov.png',
            'clients': 'imagenes/icons/clients.png',
            'addclient': 'imagenes/icons/addclient.png',
            'settings': 'imagenes/icons/settings.png',
            'user_adjust': 'imagenes/icons/user_adjust.png',
            'user_profiles': 'imagenes/icons/user_profiles.png',
            'permise': 'imagenes/icons/permise.png',
            'module': 'imagenes/icons/module.png',
            'product': 'imagenes/icons/product.png',
            'product_cat': 'imagenes/icons/product_cat.png',
            'almacen': 'imagenes/icons/almacen.png',
            'adjustdepot': 'imagenes/icons/adjustdepot.png',
            'menu': 'imagenes/icons/menu.png'
        }

        # Redimensionar imágenes y convertir a PhotoImage
        self.icons = {}

        for key, path in self.images.items():
            image = Image.open(path)
            resized_image = image.resize((WIDTH_LOGO, HEIGHT_LOGO))
            self.icons[key] = ImageTk.PhotoImage(resized_image)
    def topBarControls(self):
        # Configuración de la barra superior
        font_awesome = customtkinter.CTkFont(family='Roboto', size=12)
        
        # Etiqueta de título
        self.labelTitulo = customtkinter.CTkLabel(
            self.barra_superior, text="Menu", font=font_awesome, padx=20, text_color="white"
        )
        self.labelTitulo.configure(fg_color="transparent", font=("Roboto", 15), bg_color='transparent', pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)
        
        # Botón del menú lateral
        self.buttonMenuLateral = customtkinter.CTkButton(
            self.barra_superior, text="", image=self.icons['menu'],
            command=self.toggle_menu, bg_color='transparent', fg_color='transparent', hover=False, width=WIDTH_LOGO, height=HEIGHT_LOGO
        )
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=20)
    def menuControls(self, permisos):
        self.botones = []
        self.textos_originales = []
        self.submenu_frames = {}
        self.submenu_visible = False
        self.current_submenu_frame = None 
        self.submenu_botones_textos = {}

        logo_image = Image.open("imagenes/icons/logo.png")
        self.logo_image = ImageTk.PhotoImage(logo_image.resize((WIDTH_LOGO_MAX, HEIGHT_LOGO_MAX)))
        self.logo_min_image = ImageTk.PhotoImage(logo_image.resize((WIDTH_LOGO, HEIGHT_LOGO)))
        self.labellogo = tk.Label(self.menu_lateral, image=self.logo_min_image, bg=COLOR_MENU_LATERAL)
        self.labellogo.pack(side=tk.TOP, pady=15, padx=10)

        buttons_info = {
            'HOME1001': ('home', "Inicio", self.openFormDashboard),
            'ALMA1001': ('almacen', "Almacen", lambda: self.toggleSubmenu('ALMA1001', permisos)),
            'PROV1001': ('prov', "Proveedores", lambda: self.toggleSubmenu('PROV1001', permisos)),
            'CLIE1001': ('clients', "Clientes", lambda: self.toggleSubmenu('CLIE1001', permisos)),
            'CONF1001': ('settings', "Ajustes", lambda: self.toggleSubmenu('CONF1001', permisos))
        }

        for perm, (icon_key, text, command) in buttons_info.items():
            if perm in permisos:
                icon_image = Image.open(f"imagenes/icons/{icon_key}.png")
                icon_resized = icon_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
                icon_photo = ImageTk.PhotoImage(icon_resized)
                button = tk.Button(self.menu_lateral, text=text, font=("Roboto", 16), image=icon_photo,
                                   highlightthickness=20, width=150, height=ALTO_MENU, bg=COLOR_MENU_LATERAL,
                                   bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=command)
                button.image = icon_photo
                button.pack(fill='x')
                self.botones.append(button)
                self.textos_originales.append(text)
                binding_hover_event(button)
                
                if perm not in self.submenu_frames:
                    self.submenu_frame = tk.Frame(self.menu_lateral, bg=COLOR_SUBMENU_LATERAL)
                    self.submenu_frame.pack(fill='x')
                    self.submenu_frames[perm] = self.submenu_frame
                    self.submenu_botones_textos[perm] = {}

    def toggle_menu(self):
        self.menu_expandido = not self.menu_expandido

        if self.menu_expandido:
            # Expande el menú
            self.menu_lateral.config(width=150)
            self.labellogo.config(image=self.logo_image)  # Usa el logo en tamaño normal
            for boton, texto_original in zip(self.botones, self.textos_originales):
                boton.config(text=texto_original, width=150, anchor="w")
                binding_hover_event(boton)
            for submenu_key, submenu_frame in self.submenu_frames.items():
            # Restaura los textos originales de los botones del submenú
                for widget in submenu_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        original_text = self.submenu_botones_textos.get(submenu_key, {}).get(widget, None)
                        if original_text:
                            widget.config(text=original_text, width=150, anchor="w")
                            binding_hover_submenu_event(widget)
        else:
            # Minimiza el menú
            self.menu_lateral.config(width=50)
            self.labellogo.config(image=self.logo_min_image)  # Usa el logo en tamaño minimizado
            for boton in self.botones:
                boton.config(text="", width=50, anchor="center")
                binding_hover_event_min(boton)
            for submenu_frame in self.submenu_frames.values():
            # Asegúrate de que los botones en el submenu también se configuren correctamente al minimizar
                for widget in submenu_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.config(text="", width=50, anchor="center")  # Ajusta el tamaño al estado minimizado
                        binding_hover_submenu_event_min(widget)
    def restore_submenu_buttons_text(self):
        if not hasattr(self, 'submenu_textos_originales'):
            return
        
        for submenu_frame in self.submenu_frames.values():
            for button in submenu_frame.winfo_children():
                boton_nombre = next((name for name, widget in self.__dict__.items() if widget == button), None)
                if boton_nombre and boton_nombre in self.submenu_textos_originales:
                    button.config(text=self.submenu_textos_originales[boton_nombre], width=ANCHO_MENU)

    def hide_submenu_buttons_text(self):
        for submenu_frame in self.submenu_frames.values():
            for button in submenu_frame.winfo_children():
                # Ocultar texto del botón del submenú
                button.config(text="", width=50)
    def toggleSubmenu(self, submenu_key, permisos):
        submenu_frame = self.submenu_frames.get(submenu_key)
        if submenu_frame:
            # Cuando el menú está expandido
            if self.menu_expandido:
                # Si el submenú actual es el que está abierto, lo cerramos
                if submenu_frame == self.current_submenu_frame:
                    self.closeCurrentSubmenu()
                else:
                    # Si hay otro submenú abierto, lo cerramos
                    if self.current_submenu_frame:
                        self.closeCurrentSubmenu()
                    # Abrimos el nuevo submenú
                    self.current_submenu_frame = submenu_frame
                    self.openSubmenu(submenu_key, permisos)
                    submenu_frame.pack(fill='x')
            else:
                # Cuando el menú está contraído
                if submenu_frame == self.current_submenu_frame:
                    self.closeCurrentSubmenu()
                else:
                    # Cerrar submenús abiertos si hay uno activo
                    if self.current_submenu_frame:
                        self.closeCurrentSubmenu()
                    # Abrir el nuevo submenú
                    self.current_submenu_frame = submenu_frame
                    self.openSubmenu(submenu_key, permisos)

                    # Mantener el menú contraído pero mostrar submenús minimizados
                    submenu_frame.pack(fill='x')
                    for widget in submenu_frame.winfo_children():
                        if isinstance(widget, tk.Button):
                            widget.config(text="", width=50, anchor="center")  # Mantener submenú minimizado
                            binding_hover_submenu_event_min(widget)
    def minimize_all_submenus(self):
        for submenu_frame in self.submenu_frames.values():
            if submenu_frame:
                submenu_frame.pack_forget()
                submenu_frame.config(height=1)
    def openSubmenu(self, submenu_key, permisos):
        # Llamar a la función correspondiente para configurar el submenú
        if submenu_key == 'ALMA1001':
            self.submenuStore(permisos)
        elif submenu_key == 'PROV1001':
            self.submenuSuppliers(permisos)
        elif submenu_key == 'CLIE1001':
            self.submenuClients(permisos)
        elif submenu_key == 'CONF1001':
            self.submenuConfig(permisos)

        # Obtener el frame del submenú correspondiente
        submenu_frame = self.submenu_frames.get(submenu_key)

        if submenu_frame:
            # Cerrar el submenú anterior si existe
            if self.current_submenu_frame and self.current_submenu_frame != submenu_frame:
                self.closeCurrentSubmenu()

            # Guardar los textos originales de los botones si aún no se han guardado
            for widget in submenu_frame.winfo_children():
                if isinstance(widget, tk.Button):
                    if widget not in self.submenu_botones_textos[submenu_key]:
                        self.submenu_botones_textos[submenu_key][widget] = widget.cget("text")

            # Establecer el nuevo submenú actual
            self.current_submenu_frame = submenu_frame

            # Si el menú lateral está contraído, mostrar solo los íconos
            if not self.menu_expandido:
                for widget in submenu_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.config(text="", width=50, anchor="center")
                        binding_hover_submenu_event_min(widget)
            else:
                # Si el menú está expandido, restaurar los textos de los botones
                for widget in submenu_frame.winfo_children():
                    if isinstance(widget, tk.Button) and widget in self.submenu_botones_textos[submenu_key]:
                        widget.config(text=self.submenu_botones_textos[submenu_key][widget], width=150, anchor="w")
                        binding_hover_submenu_event(widget)

            # Mostrar el frame del submenú
            submenu_frame.pack(fill='x')
    def closeCurrentSubmenu(self):
        if self.current_submenu_frame:
            # Ocultar los widgets del submenú actual
            for widget in self.current_submenu_frame.winfo_children():
                widget.pack_forget()

            # Minimizar el frame del submenú
            self.current_submenu_frame.config(height=1)
            self.current_submenu_frame.update_idletasks()  # Actualizar la interfaz

            if not self.menu_expandido:
                # Si el menú está contraído, ajustar los botones a su formato minimizado
                for widget in self.current_submenu_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.config(text="", width=50, anchor="center")
                        binding_hover_submenu_event_min(widget)

            self.current_submenu_frame = None 

    def submenuStore(self, permisos):
        # Diccionario de configuración de botones para submenú Almacen
        botones_submenu = {
            'ALMA1002': ('buttonDepositos', "Depositos", self.icons['adjustdepot'], lambda: self.openFormDepots(permisos)),
            'ALMA1003': ('buttonProductos', "Productos", self.icons['product'], lambda: self.openFormProducts(permisos)),
            'ALMA1004': ('buttonCatArt', "Categoria de\nProductos", self.icons['product_cat'], lambda: self.openFormCategory(permisos))
        }

        submenu_frame = self.submenu_frames.get('ALMA1001')
        if submenu_frame:
            # Limpieza de submenú Almacen
            for permiso, (boton_nombre, _, _, _) in botones_submenu.items():
                if hasattr(self, boton_nombre):
                    getattr(self, boton_nombre).pack_forget()
                    delattr(self, boton_nombre)
            
            self.submenu_textos_originales = {}

            # Inicialización del submenú Almacen basado en permisos
            for permiso, (boton_nombre, texto, icono, comando) in botones_submenu.items():
                if permiso in permisos:
                    if not hasattr(self, boton_nombre):  # Solo crea botones si no existen
                        boton = tk.Button(submenu_frame, text=texto, font=("Roboto", 12), image=icono, highlightthickness=20,
                                          width=ANCHO_MENU, bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white",
                                          anchor="w", compound=tk.LEFT, padx=10, command=comando)
                        boton.pack()
                        binding_hover_submenu_event(boton)
                        setattr(self, boton_nombre, boton)
                        self.submenu_textos_originales[boton_nombre] = texto
                    else:
                        getattr(self, boton_nombre).pack()

    def submenuSuppliers(self, permisos):
        # Diccionario de configuración de botones para submenú Proveedores
        botones_submenu = {
            'PROV1002': ('buttonProveedor', "Listado de\nProveedores", self.icons['listprov'], lambda: self.openFormSuppliers(permisos)),
        }

        submenu_frame = self.submenu_frames.get('PROV1001')
        if submenu_frame:
            # Limpieza de submenú Proveedores
            for permiso, (boton_nombre, _, _, _) in botones_submenu.items():
                if hasattr(self, boton_nombre):
                    getattr(self, boton_nombre).pack_forget()
                    delattr(self, boton_nombre)

            self.submenu_textos_originales = {}

            # Inicialización del submenú Proveedores basado en permisos
            for permiso, (boton_nombre, texto, icono, comando) in botones_submenu.items():
                if permiso in permisos:
                    if not hasattr(self, boton_nombre):  # Solo crea botones si no existen
                        boton = tk.Button(submenu_frame, text=texto, font=("Roboto", 12), image=icono, highlightthickness=20,
                                          width=ANCHO_MENU, bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white",
                                          anchor="w", compound=tk.LEFT, padx=10, command=comando)
                        boton.pack()
                        binding_hover_submenu_event(boton)
                        setattr(self, boton_nombre, boton)
                        self.submenu_textos_originales[boton_nombre] = texto
                    else:
                        getattr(self, boton_nombre).pack()
    def submenuConfig(self, permisos):
        # Configuración de botones para el submenú de Ajustes
        botones_submenu = {
        'CONF1002': ('buttonUsuarios', "Usuarios", self.icons['user_adjust'], lambda: self.openFormUser(permisos)),
        'CONF1003': ('buttonProfiles', "Perfiles", self.icons['user_profiles'], lambda: self.openFormAdjustProfile(permisos)),
        'CONF1004': ('buttonModules', "Modulos", self.icons['module'], lambda: self.openFormModules(permisos)),
        'CONF1005': ('buttonPermiss', "Permisos", self.icons['permise'], lambda: self.openFormPermission(permisos))
    }
        submenu_frame = self.submenu_frames.get('CONF1001')
        if submenu_frame:
            # Limpieza de submenú Configuración
            for permiso, (boton_nombre, _, _, _) in botones_submenu.items():
                if hasattr(self, boton_nombre):
                    getattr(self, boton_nombre).pack_forget()
                    delattr(self, boton_nombre)

            self.submenu_textos_originales = {}

            # Inicialización del submenú Configuración basado en permisos
            for permiso, (boton_nombre, texto, icono, comando) in botones_submenu.items():
                if permiso in permisos:
                    if not hasattr(self, boton_nombre):  # Solo crea botones si no existen
                        boton = tk.Button(submenu_frame, text=texto, font=("Roboto", 12), image=icono, highlightthickness=20,
                                          width=ANCHO_MENU, bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white",
                                          anchor="w", compound=tk.LEFT, padx=10, command=comando)
                        boton.pack()
                        binding_hover_submenu_event(boton)
                        setattr(self, boton_nombre, boton)
                        self.submenu_textos_originales[boton_nombre] = texto
                    else:
                        getattr(self, boton_nombre).pack()

    def submenuClients(self, permisos):
        # Diccionario de configuración de botones para submenú Clientes
        botones_submenu = {
            'CLIE1002': ('buttonClientes', "Lista de Clientes", self.icons['addclient'], lambda: self.openFormRegClient(permisos)),
        }

        submenu_frame = self.submenu_frames.get('CLIE1001')
        if submenu_frame:
            # Limpieza de submenú Clientes
            for permiso, (boton_nombre, _, _, _) in botones_submenu.items():
                if hasattr(self, boton_nombre):
                    getattr(self, boton_nombre).pack_forget()
                    delattr(self, boton_nombre)

            self.submenu_textos_originales = {}

            # Inicialización del submenú Clientes basado en permisos
            for permiso, (boton_nombre, texto, icono, comando) in botones_submenu.items():
                if permiso in permisos:
                    if not hasattr(self, boton_nombre):  # Solo crea botones si no existen
                        boton = tk.Button(submenu_frame, text=texto, font=("Roboto", 12), image=icono, highlightthickness=20,
                                          width=ANCHO_MENU, bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white",
                                          anchor="w", compound=tk.LEFT, padx=10, command=comando)
                        boton.pack()
                        binding_hover_submenu_event(boton)
                        setattr(self, boton_nombre, boton)
                        self.submenu_textos_originales[boton_nombre] = texto
                    else:
                        getattr(self, boton_nombre).pack()
                
    def loginSection(self):
        self.w, self.h = 800, 600
        centerWidget(self)
        loadBackgroundImage(self)

        frame_login = customtkinter.CTkFrame(self.cuerpo_principal, fg_color="white", width=300, height=250)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(frame_login, 0.9)
        #Iconos
        user_ico = Image.open("imagenes/icons/user.png")
        user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        user_img = ImageTk.PhotoImage(user_ico)

        pass_ico = Image.open("imagenes/icons/pass.png")
        pass_ico = pass_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        pass_img = ImageTk.PhotoImage(pass_ico)

        #LOGIN USER
        lbluser = customtkinter.CTkLabel(frame_login, text="", image=user_img, bg_color="white")
        lbluser.pack(pady=1, padx=6)
        lbluser.place(x=55, y=55)
        
        set_opacity(lbluser, 0.8)

        self.sv_datauser = customtkinter.StringVar()
        style = ttk.Style()
        style.configure("Custom.TEntry", borderwidth=0)

        entryuser = ttk.Entry(frame_login, textvariable=self.sv_datauser, width=14, font=("Arial", 12), style="Custom.TEntry", justify="center")
        entryuser.place(x=105, y=56)
        #LOGIN PASSWORD
        lblpass = customtkinter.CTkLabel(frame_login, text="", image=pass_img, bg_color="white")
        lblpass.pack(pady=1, padx=6)
        lblpass.place(x=55, y=125)

        set_opacity(lblpass, 0.8)

        self.sv_datapass = customtkinter.StringVar()
        #entrypass = customtkinter.CTkEntry(self.cuerpo_principal, textvariable=sv_datapass, show="*", width=150)
        entrypass = ttk.Entry(frame_login, textvariable=self.sv_datapass, width=14, font=("Arial", 13), style="Custom.TEntry", show="*", justify="center")
        entrypass.place(x=105, y=126)
        entrypass.bind("<Return>", lambda event: self.validateLogin())
        
        #LOGIN BOTON
        stylebutton = ttk.Style()
        stylebutton.configure("Custom.TButton")
        btnLogIn = ttk.Button(frame_login, text="Iniciar Sesion", command=self.validateLogin, width=14, style="Custom.TButton")
        btnLogIn.place(x=120, y=180)
    def validateLogin(self):
        conexion = ConexionDB()
        username = self.sv_datauser.get()
        password = self.sv_datapass.get()
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
            self.cuerpo_principal.destroy()
            self.initializeMainApp(idrol)
        else:
            login_wrong_advice()
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
            return permisos
        else:
            return None
    def initializeMainApp(self, idrol):
        self.w, self.h = 1440, 900
        self.geometry(f"{self.w}x{self.h}")
        self.resizable(True, True)
        util_screen.center_screen(self, self.w, self.h)
        permisos = self.get_idrol(idrol)
        self.createPanels()
        self.menuControls(permisos)
        self.topBarControls()
        self.openFormDashboard()
        self.menu_expandido = True
        self.toggle_menu()
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

