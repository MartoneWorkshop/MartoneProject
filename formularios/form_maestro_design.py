import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_FONDO, COLOR_MENU_CURSOR_ENCIMA, COLOR_SUBMENU_LATERAL, COLOR_SUBMENU_CURSOR_ENCIMA, ANCHO_MENU, MITAD_MENU, ALTO_MENU, WIDTH_LOGO, HEIGHT_LOGO
from PIL import Image, ImageTk
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from customtkinter import *
import customtkinter
import ctypes
import pystray
import win32api
import win32con
import win32gui
from pystray import MenuItem as item, Icon

from formularios.form_registros_design import FormularioRegistrosDesign
from formularios.form_home_design import FormularioHomeDesign

class FormularioMaestroDesign(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/logo.png", (590, 423))
        self.bg = util_img.leer_imagen("./imagenes/bg.jpg", (1440, 900))
        self.perfil = util_img.leer_imagen("./imagenes/Perfil.png", (100, 100))
        
        self.w, self.h = 1440, 900
        self.title("Martone Workshop - Registro")
        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.set_window_icon()
        self.w, self.h = 1440, 900
        self.geometry(f"{self.w}x{self.h}")
        self.iconbitmap("./imagenes/logo.ico")   
        util_ventana.centrar_ventana(self, self.w, self.h)

    def paneles(self):        
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_FONDO)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def set_window_icon(self):
        icon_path = "imagenes/logo.ico"  # Ruta del archivo de icono
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("martoneworkshop")  # Cambia "myappid" por un identificador único para tu aplicación
        self.iconbitmap(icon_path)

    def on_exit(icon, item):
        icon.stop()
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = customtkinter.CTkFont(family='Roboto', size=12)

        # Etiqueta de título
        self.labelTitulo = customtkinter.CTkLabel(self.barra_superior, text="Martone Workshop", font=font_awesome,padx=20, text_color="white")
        self.labelTitulo.configure(fg_color="transparent", font=(
            "Roboto", 15), bg_color='transparent', pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        self.menu_original_image = Image.open("imagenes/menu.png")
        self.menu_resized_image = self.menu_original_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.menu_image = ImageTk.PhotoImage(self.menu_resized_image)
        # Botón del menú lateral
        self.buttonMenuLateral = customtkinter.CTkButton(self.barra_superior, text="", image=self.menu_image,
                                        command=self.toggle_panel, bg_color='transparent', fg_color='transparent', hover=False, width=WIDTH_LOGO, height=HEIGHT_LOGO)
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=20)

        #close_original_image = Image.open("imagenes/close.png")
        #close_resized_image = close_original_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #close_image = ImageTk.PhotoImage(close_resized_image)
#
        #self.btnCloseW = customtkinter.CTkButton(self.barra_superior, image=close_image, text="", fg_color='transparent', bg_color='transparent', height=HEIGHT_LOGO, width=WIDTH_LOGO, command=self.close_window)
        #self.btnCloseW.pack(side=tk.RIGHT, padx=20)
#
        ################################################## MINIMIZAR
        #original_image = Image.open("imagenes/min.png")
#
        #resized_image = original_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #image = ImageTk.PhotoImage(resized_image)
        #self.btnMinW = customtkinter.CTkButton(self.barra_superior, image=image, text="", fg_color='transparent', bg_color='transparent', height=HEIGHT_LOGO, width=WIDTH_LOGO, command=self.minimize_window)
        #self.btnMinW.pack(side=tk.RIGHT)
        
    def controles_menu_lateral(self):
        self.id_client = None
        # ESTO AUN NO ESTA DEFINIDO
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
        #IMAGENES RENDERIZADAS
        home_resized = home_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        registros_resized = registros_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        clientes_resized = clientes_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        equipos_resized = equipos_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        historia_resized = historia_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        database_resized = database_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        informes_resized = informes_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        settings_resized = settings_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        #IMAGENES FINALES
        self.home_icon = ImageTk.PhotoImage(home_resized)
        self.registros_icon = ImageTk.PhotoImage(registros_resized)
        self.clientes_icon = ImageTk.PhotoImage(clientes_resized)
        self.equipos_icon = ImageTk. PhotoImage(equipos_resized)
        self.historia_icon = ImageTk.PhotoImage(historia_resized)
        self.database_icon = ImageTk.PhotoImage(database_resized)
        self.informes_icon = ImageTk.PhotoImage(informes_resized)
        self.settings_icon = ImageTk.PhotoImage(settings_resized)
        #BOTONES DEL MENU
        self.buttonHome = tk.Button(self.menu_lateral, text="Home", font=("Roboto", 16), image=self.home_icon, highlightthickness=20, width=ANCHO_MENU,
            height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.abrir_home)
        self.buttonHome.pack()

        self.buttonRegistro = tk.Button(self.menu_lateral, text="Registros", font=("Roboto", 16), image=self.registros_icon, highlightthickness=20, width=ANCHO_MENU,
            height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.submenu_registros)
        self.buttonRegistro.pack() 

        self.buttonDatabase = tk.Button(self.menu_lateral, text="Database",  font=("Roboto", 16),image=self.database_icon, highlightthickness=20, width=ANCHO_MENU,
            height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)
        self.buttonDatabase.pack()

        self.buttonInformes = tk.Button(self.menu_lateral, text="Informes",  font=("Roboto", 16),image=self.informes_icon, highlightthickness=20, width=ANCHO_MENU,
            height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)        
        self.buttonInformes.pack() 

        self.buttonSettings = tk.Button(self.menu_lateral, text="Settings",  font=("Roboto", 16),image=self.settings_icon, highlightthickness=20, width=ANCHO_MENU,
            height=ALTO_MENU, bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10)
        self.buttonSettings.pack()
        #ASIGNACION DE EFECTOS
        self.binding_hover_event(self.buttonHome)
        self.binding_hover_event(self.buttonRegistro)
        self.binding_hover_event(self.buttonDatabase)
        self.binding_hover_event(self.buttonInformes)
        self.binding_hover_event(self.buttonSettings)

    def submenu_registros(self):
        self.buttonDatabase.pack_forget()
        self.buttonInformes.pack_forget()
        self.buttonSettings.pack_forget()

        if hasattr(self, "buttonClientes"):
            self.buttonClientes.pack_forget()
            del self.buttonClientes
        if hasattr(self, "buttonEquipos"):
            self.buttonEquipos.pack_forget()
            del self.buttonEquipos
        if hasattr(self, "buttonHistoria"):
            self.buttonHistoria.pack_forget()
            del self.buttonHistoria

        else:
            self.buttonClientes = tk.Button(self.menu_lateral, text="Clientes", font=("Roboto", 12), image=self.clientes_icon, highlightthickness=20, width=ANCHO_MENU,
        bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.abrir_registros_clientes)
            self.buttonClientes.pack()

            self.buttonEquipos = tk.Button(self.menu_lateral, text="Equipos", font=("Roboto", 12), image=self.equipos_icon, highlightthickness=20, width=ANCHO_MENU,
        bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10)
            self.buttonEquipos.pack()

            self.buttonHistoria = tk.Button(self.menu_lateral, text="Historia", font=("Roboto", 12), image=self.historia_icon, highlightthickness=20, width=ANCHO_MENU,
        bd=0, height=MITAD_MENU, bg=COLOR_SUBMENU_LATERAL, fg="white", anchor="w", compound=tk.LEFT, padx=10)
            self.buttonHistoria.pack()

        self.buttonDatabase.pack()
        self.buttonInformes.pack()
        self.buttonSettings.pack()

        self.binding_hover_submenu_event(self.buttonClientes)
        self.binding_hover_submenu_event(self.buttonEquipos)
        self.binding_hover_submenu_event(self.buttonHistoria)

    def controles_cuerpo(self):
        self.abrir_home()

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


    def abrir_home(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioHomeDesign(self.cuerpo_principal,self.bg) 

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
