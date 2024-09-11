import ctypes
from ctypes import windll
import tkinter as tk
from PIL import Image, ImageTk
from config import COLOR_BARRA_SUPERIOR, COLOR_BG, COLOR_BOTON_CURSOR_ENCIMA, COLOR_BOTON_CURSOR_FUERA, COLOR_EDITAR,COLOR_ELIMINAR, COLOR_FG, COLOR_FONDO, COLOR_GUARDAR,COLOR_HOVER, COLOR_LIMPIAR,COLOR_MENU_CURSOR_ENCIMA,COLOR_MENU_LATERAL, COLOR_SUBMENU_CURSOR_ENCIMA,COLOR_SUBMENU_LATERAL,COLOR_TEXTO,ANCHO_MENU,ALTO_MENU,MITAD_MENU

def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):    
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (aplicacion_ancho/2))
    y = int((pantall_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
def set_window_icon(self):
    icon_path = "imagenes/icons/logo_ico.ico"  # Ruta del archivo de icono
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("HAST")  # Cambia "myappid" por un identificador único para tu aplicación
    self.iconbitmap(icon_path)
def set_opacity(widget, value: float):
    widget = widget.winfo_id()
    value = int(255*value) # value from 0 to 1
    wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
    new_exstyle = wnd_exstyle | 0x00080000  
    windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
    windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)
def binding_hover_event(button):
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))
def on_enter(event, button):
    button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white', anchor="w")
def on_leave(event, button):
    button.config(bg=COLOR_MENU_LATERAL, fg='white', anchor="w")
def binding_hover_event_min(button):
    button.bind("<Enter>", lambda event: on_enter_min(event, button))
    button.bind("<Leave>", lambda event: on_leave_min(event, button))
def on_enter_min(event, button):
    button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')
def on_leave_min(event, button):
    button.config(bg=COLOR_MENU_LATERAL, fg='white')

def binding_hover_submenu_event(button):
    button.bind("<Enter>", lambda event: submenu_on_enter(event, button))
    button.bind("<Leave>", lambda event: submenu_on_leave(event, button))
def submenu_on_enter(event, button):
    button.config(bg=COLOR_SUBMENU_CURSOR_ENCIMA, fg='white', anchor="w", height=ALTO_MENU)
def submenu_on_leave(event, button):
    button.config(bg=COLOR_SUBMENU_LATERAL, fg='white', anchor="w", height=MITAD_MENU)

def binding_hover_submenu_event_min(button):
    button.bind("<Enter>", lambda event: submenu_on_enter_min(event, button))
    button.bind("<Leave>", lambda event: submenu_on_leave_min(event, button))
def submenu_on_enter_min(event, button):
    button.config(bg=COLOR_SUBMENU_CURSOR_ENCIMA, fg='white', anchor="center", height=ALTO_MENU)
def submenu_on_leave_min(event, button):
    button.config(bg=COLOR_SUBMENU_LATERAL, fg='white', anchor="center", height=MITAD_MENU)
    
def cleanPanel(panel):
# Función para limpiar el contenido del panel
    for widget in panel.winfo_children():
        widget.destroy()
def centerWindow(self):
    self.update_idletasks()
    width = self.w
    height = self.h
    screenwidth = self.winfo_screenwidth()
    screenheight = self.winfo_screenheight()
    x = (screenwidth / 2) - (width / 2)
    y = (screenheight / 2) - (height / 2)
    self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
def loadBackgroundImage(self):
    # Cargar y ajustar imagen de fondo
    ruta_imagen = "imagenes/bg1.jpeg"
    imagen = Image.open(ruta_imagen)
    imagen_tk = ImageTk.PhotoImage(imagen)
    self.imagen_tk = imagen_tk
    label_fondo = tk.Label(self.cuerpo_principal, image=imagen_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    self.label_fondo = label_fondo
    def adjustImage(event):
        nueva_imagen = imagen.resize((event.width, event.height))
        nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
        self.imagen_tk = nueva_imagen_tk
        label_fondo.config(image=nueva_imagen_tk)
    self.cuerpo_principal.bind("<Configure>", adjustImage)

