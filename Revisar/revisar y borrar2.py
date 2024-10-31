import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from PIL import Image, ImageTk
import util.util_screen as util_screen
import util.util_imagenes as util_img
from customtkinter import *
import customtkinter
import ctypes
import win32gui
import pystray
import pystray
import win32api
import win32con
import win32gui
from pystray import MenuItem as item, Icon


class FormularioMaestroDesign(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/logo.png", (590, 423))
        self.perfil = util_img.leer_imagen("./imagenes/Perfil.png", (100, 100))
        self.w, self.h = 1440, 900
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
        self.w, self.h = 1440, 900        
        util_screen.center_screen(self, self.w, self.h)
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.move_window)
        self.bind("<Map>", self.on_restore)

    def on_restore(self, event):
        if self.wm_state() == "normal":
            self.overrideredirect(True)

    def paneles(self):        
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def close_window(self):
        self.destroy()

    def start_move(self, event):
        # Inicia el movimiento de la ventana
        self.x = event.x
        self.y = event.y

    def move_window(self, event):
        # Mueve la ventana según el movimiento del ratón
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def minimize_window(self):
        self.overrideredirect(False)
        self.iconify()
        win32gui.SetWindowText(win32gui.GetForegroundWindow(), "MartoneWorkshop")
    
    def set_window_icon(self):
        icon_path = "./imagenes/logo.ico"  # Ruta del archivo de icono
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("martoneworkshop")  # Cambia "myappid" por un identificador único para tu aplicación
        self.iconbitmap(icon_path)

    def on_exit(icon, item):
        icon.stop()
    
    # Configura el icono y las acciones


    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = customtkinter.CTkFont(family='Roboto', size=12)

        # Etiqueta de título
        self.labelTitulo = customtkinter.CTkLabel(self.barra_superior, text="Martone Workshop", font=font_awesome,padx=20, text_color="white")
        self.labelTitulo.configure(fg_color="transparent", font=(
            "Roboto", 15), bg_color='transparent', pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        self.menu_original_image = Image.open("imagenes/menu.png")
        self.width = 25
        self.height = 25
        self.menu_resized_image = self.menu_original_image.resize((self.width, self.height))
        self.menu_image = ImageTk.PhotoImage(self.menu_resized_image)
        # Botón del menú lateral
        self.buttonMenuLateral = customtkinter.CTkButton(self.barra_superior, text="", image=self.menu_image,
                                        command=self.toggle_panel, bg_color='transparent', fg_color='transparent', hover=False, width=25, height=25)
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=20)


        close_original_image = Image.open("imagenes/close.png")
        width = 25
        height = 25
        close_resized_image = close_original_image.resize((width, height))
        close_image = ImageTk.PhotoImage(close_resized_image)

        self.btnCloseW = customtkinter.CTkButton(self.barra_superior, image=close_image, text="", fg_color='transparent', bg_color='transparent', height=25, width=25, command=self.close_window)
        self.btnCloseW.pack(side=tk.RIGHT, padx=20)

        ################################################# MINIMIZAR
        original_image = Image.open("imagenes/min.png")
        width = 25
        height = 25
        resized_image = original_image.resize((width, height))
        image = ImageTk.PhotoImage(resized_image)
        self.btnMinW = customtkinter.CTkButton(self.barra_superior, image=image, text="", fg_color='transparent', bg_color='transparent', height=25, width=25, command=self.minimize_window)
        self.btnMinW.pack(side=tk.RIGHT)
        
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 165
        alto_menu = 40
        #20 / 2
        # Etiqueta de perfil
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        width = 25
        height = 25

        # Botones del menú lateral
        home_image = Image.open("imagenes/home.png") 
        registros_image = Image.open("imagenes/register.png")
        database_image = Image.open("imagenes/database.png")
        informes_image = Image.open("imagenes/reportes.png")
        settings_image = Image.open("imagenes/settings.png")    

        home_resized = home_image.resize((width, height))
        registros_resized = registros_image.resize((width, height))
        database_resized = database_image.resize((width, height))
        informes_resized = informes_image.resize((width, height))
        settings_resized = settings_image.resize((width, height))

        home_icon = ImageTk. PhotoImage(home_resized)
        registros_icon = ImageTk. PhotoImage(registros_resized)
        database_icon = ImageTk. PhotoImage(database_resized)
        informes_icon = ImageTk. PhotoImage(informes_resized)
        settings_icon = ImageTk. PhotoImage(settings_resized)

        self.buttonHome = tk.Button(self.menu_lateral, text="Home", image=home_icon, width=ancho_menu, height=alto_menu, bg=COLOR_MENU_LATERAL, fg="white", anchor="w", padx=15)        
        self.buttonRegistro = tk.Button(self.menu_lateral)
        self.buttonDatabase = tk.Button(self.menu_lateral)
        self.buttonInformes = tk.Button(self.menu_lateral)        
        self.buttonSettings = tk.Button(self.menu_lateral)
       
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                    bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, icon, ancho_menu, alto_menu):
        button.image = icon
        button.config(text=f"{text}", padx=15, font=("Roboto", 16), anchor="w", image=icon, compound=tk.LEFT,
                    bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)

        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')