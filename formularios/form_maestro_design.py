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
from formularios.form_registros_design import FormularioRegistrosDesign
from formularios.form_home_design import FormularioHomeDesign
from formularios.form_users import FormUsers
from formularios.form_modulos import FormModulos
class FormularioMaestroDesign(customtkinter.CTk):
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
        self.bg = util_img.leer_imagen("./imagenes/bg.png", (1440, 900))
        self.title("Policlinica de Especialidades")
        self.set_window_icon()
        self.w, self.h = 800, 600
        self.geometry(f"{self.w}x{self.h}")
        self.resizable(False, False)
        self.iconbitmap("./imagenes/Logo_Ico.ico")   
        util_ventana.centrar_ventana(self, self.w, self.h)
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
        icon_path = "imagenes/logo_ico.ico"  # Ruta del archivo de icono
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PECA-GesInv")  # Cambia "myappid" por un identificador único para tu aplicación
        self.iconbitmap(icon_path)
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = customtkinter.CTkFont(family='Roboto', size=12)
        # Etiqueta de título
        self.labelTitulo = customtkinter.CTkLabel(self.barra_superior, text="Gestion de Inventario", font=font_awesome,padx=20, text_color="white")
        self.labelTitulo.configure(fg_color="transparent", font=("Roboto", 15), bg_color='transparent', pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)
        self.menu_original_image = Image.open("imagenes/menu.png")
        self.menu_resized_image = self.menu_original_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.menu_image = ImageTk.PhotoImage(self.menu_resized_image)
        # Botón del menú lateral
        self.buttonMenuLateral = customtkinter.CTkButton(self.barra_superior, text="", image=self.menu_image,
                                        command=self.toggle_panel, bg_color='transparent', fg_color='transparent', hover=False, width=WIDTH_LOGO, height=HEIGHT_LOGO)
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=20)
    def controles_menu_lateral(self, permisos):
        self.perfil = util_img.leer_imagen("./imagenes/logo.png", (100, 100))
        ## ESTO AUN NO ESTA DEFINIDO42
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)
        #RUTAS DE LAS IMAGENES
        home_image = Image.open("imagenes/home.png") 
        registros_image = Image.open("imagenes/register.png")
        clientes_image = Image.open("imagenes/person.png")
        equipos_image = Image.open("imagenes/computer.png")
        historia_image = Image.open("imagenes/history.png")
        database_image = Image.open("imagenes/database.png")
        informes_image = Image.open("imagenes/reporte.png")
        settings_image = Image.open("imagenes/settings.png")
        usuarios_image = Image.open("imagenes/usuarios.png")
        adjustUser_image = Image.open("imagenes/user_adjust.png")   

        #IMAGENES RENDERIZADAS
        home_resized = home_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        registros_resized = registros_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        clientes_resized = clientes_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        equipos_resized = equipos_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        historia_resized = historia_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        database_resized = database_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        informes_resized = informes_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        settings_resized = settings_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        usuarios_resized = usuarios_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        adjustUser_resized = adjustUser_image.resize((WIDTH_LOGO, HEIGHT_LOGO)) 
        #IMAGENES FINALES
        self.home_icon = ImageTk.PhotoImage(home_resized)
        self.registros_icon = ImageTk.PhotoImage(registros_resized)
        self.clientes_icon = ImageTk.PhotoImage(clientes_resized)
        self.equipos_icon = ImageTk. PhotoImage(equipos_resized)
        self.historia_icon = ImageTk.PhotoImage(historia_resized)
        self.database_icon = ImageTk.PhotoImage(database_resized)
        self.informes_icon = ImageTk.PhotoImage(informes_resized)
        self.settings_icon = ImageTk.PhotoImage(settings_resized)
        self.usuarios_icon = ImageTk.PhotoImage(usuarios_resized)
        self.adjustUser_icon = ImageTk.PhotoImage(adjustUser_resized)
        #BOTONES DEL MENU

        if 'HOME1000' in permisos:
            self.buttonHome = tk.Button(self.menu_lateral, text="Inicio", font=("Roboto", 16), image=self.home_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.abrir_home)
            self.buttonHome.pack()
            self.binding_hover_event(self.buttonHome)
        else:
            pass

        if 'REG1000' in permisos:
            self.buttonRegistro = tk.Button(self.menu_lateral, text="Registros", font=("Roboto", 16), image=self.registros_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenu_registros(permisos))
            self.buttonRegistro.pack()
            self.binding_hover_event(self.buttonRegistro) 
        else:
            pass

        if 'DATA100' in permisos:
            self.buttonDatabase = tk.Button(self.menu_lateral, text="Database",  font=("Roboto", 16),image=self.database_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)
            self.buttonDatabase.pack()
            self.binding_hover_event(self.buttonDatabase)
        else:
            pass
        if 'REP1000' in permisos:
            self.buttonInformes = tk.Button(self.menu_lateral, text="Informes",  font=("Roboto", 16),image=self.informes_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)        
            self.buttonInformes.pack()
            self.binding_hover_event(self.buttonInformes)
        else:
            pass
        
        if 'CON1000' in permisos:
            self.buttonSettings = tk.Button(self.menu_lateral, text="Settings",  font=("Roboto", 16),image=self.settings_icon, highlightthickness=20, width=ANCHO_MENU,
                height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.submenu_config(permisos))
            self.buttonSettings.pack()
            self.binding_hover_event(self.buttonSettings)
        else:
            pass

    def seccion_login(self):
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
        logo_image = Image.open("imagenes/logo_completo.png")
        logo_resized = logo_image.resize((205, 55))
        self.logo_final = ImageTk.PhotoImage(logo_resized)

        #Iconos
        user_ico = Image.open("imagenes/user.png")
        user_ico = user_ico.resize((20, 20))  # Cambiar el tamaño si es necesario
        user_img = ImageTk.PhotoImage(user_ico)

        pass_ico = Image.open("imagenes/pass.png")
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
        conexion = ConexionDB()
        sql = f"SELECT codpermiso FROM asigperm WHERE idrol = '{idrol}'"
        conexion.ejecutar_consulta(sql)
        resultados = conexion.obtener_resultados()
        permisos = []
        for resultado in resultados:
            permisos.append(resultado[0])
        if permisos:
            #self.prueba_menu_lateral(permisos)
            self.controles_menu_lateral(permisos)
            print(permisos)
        else:
            return None
    
    def submenu_registros(self, permisos):
        #VERIFICAR LOS PERMISOS Y QUE BOTONES ESTAN DISPONIBLES  
        if 'DATA100' in permisos:
            self.buttonDatabase.pack_forget()
        if 'REP1000' in permisos:
            self.buttonInformes.pack_forget()
        if 'CON1000' in permisos:
            self.buttonSettings.pack_forget()
        if 'USER1000' in permisos:
            if hasattr(self, "buttonAdjustUsers"):
                self.buttonAdjustUsers.pack_forget()
                del self.buttonAdjustUsers
                
        if 'MED101' in permisos:
            if hasattr(self, "buttonClientes"):
                self.buttonClientes.pack_forget()
                del self.buttonClientes
            else:
                self.buttonClientes = tk.Button(self.menu_lateral, text="Clientes", font=("Roboto", 12), image=self.clientes_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.abrir_registros_clientes)
                self.buttonClientes.pack()
                self.binding_hover_submenu_event(self.buttonClientes)
        if 'MED102' in permisos:
            if hasattr(self, "buttonEquipos"):
                self.buttonEquipos.pack_forget()
                del self.buttonEquipos
            else:
                self.buttonEquipos = tk.Button(self.menu_lateral, text="Equipos", font=("Roboto", 12), image=self.equipos_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10)
                self.buttonEquipos.pack()
                self.binding_hover_submenu_event(self.buttonEquipos)
        if 'MED103' in permisos:
            if hasattr(self, "buttonHistoria"):
                self.buttonHistoria.pack_forget()
                del self.buttonHistoria
            else:
                self.buttonHistoria = tk.Button(self.menu_lateral, text="Historia", font=("Roboto", 12), image=self.historia_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10)
                self.buttonHistoria.pack()
                self.binding_hover_submenu_event(self.buttonHistoria)
        
        if 'DATA100' in permisos:
            self.buttonDatabase.pack()
        else:
            pass
        if 'REP1000' in permisos:
            self.buttonInformes.pack()
        else:
            pass
        if 'CON1000' in permisos:
            self.buttonSettings.pack()
        else:
            pass
        if 'USER1000' in permisos:
            self.buttonAdjustUsers.pack()
        else:
            pass
    def submenu_config(self, permisos):
        if 'MED101' in permisos:
            if hasattr(self, "buttonClientes"):
                self.buttonClientes.pack_forget()
                del self.buttonClientes
            else:
                pass
        if 'MED102' in permisos:
            if hasattr(self, "buttonEquipos"):
                self.buttonEquipos.pack_forget()
                del self.buttonEquipos
            else:
                pass
        if 'MED103' in permisos:
            if hasattr(self, "buttonHistoria"):
                self.buttonHistoria.pack_forget()
                del self.buttonHistoria
            else:
                pass
        if 'USER1000' in permisos:
            if hasattr(self, "buttonAdjustUsers"):
                self.buttonAdjustUsers.pack_forget()
                del self.buttonAdjustUsers
            else:
                self.buttonAdjustUsers = tk.Button(self.menu_lateral, text="Ajuste de Usuario", font=("Roboto", 12), image=self.adjustUser_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=lambda: self.abrir_crear_usuarios(permisos))
                self.buttonAdjustUsers.pack()
                self.binding_hover_submenu_event(self.buttonAdjustUsers)

        if 'CON1001' in permisos:
            if hasattr(self, "buttonModulos"):
                self.buttonModulos.pack_forget()
                del self.buttonModulos
            else:
                self.buttonModulos = tk.Button(self.menu_lateral, text="Modulos Menu", font=("Roboto", 12), image=self.adjustUser_icon, highlightthickness=20, width=ANCHO_MENU,
                    bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10)
                self.buttonModulos.pack()
                self.binding_hover_submenu_event(self.buttonModulos)

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
    
    def abrir_registros_clientes(self):
        self.limpiar_panel(self.cuerpo_principal)
        width_screen, height_screen = self.check_size()
        if width_screen > 1440 and height_screen > 900:
            FormularioRegistrosDesign(self.cuerpo_principal, width_screen, height_screen).call_resize(width_screen, height_screen)
        elif width_screen <= 1440 and height_screen <= 900:
            FormularioRegistrosDesign(self.cuerpo_principal,width_screen, height_screen)

    def abrir_crear_usuarios(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormUsers(self.cuerpo_principal, permisos)
    def abir_modulos(self, permisos):
        self.limpiar_panel(self.cuerpo_principal)
        FormModulos(self.cuerpo_principal, permisos)
    def abrir_home(self):   
        self.limpiar_panel(self.cuerpo_principal)
        FormularioHomeDesign(self.cuerpo_principal, self.bg) 
        
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