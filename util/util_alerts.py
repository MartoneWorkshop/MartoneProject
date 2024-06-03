import tkinter as tk
from config import  COLOR_FONDO
import customtkinter
import ctypes
from  ctypes import windll
from PIL import Image, ImageTk
def set_opacity(widget, value: float):
    widget = widget.winfo_id()
    value = int(255*value) # value from 0 to 1
    wnd_exstyle = windll.user32.GetWindowLongA(widget, -20)
    new_exstyle = wnd_exstyle | 0x00080000  
    windll.user32.SetWindowLongA(widget, -20, new_exstyle)  
    windll.user32.SetLayeredWindowAttributes(widget, 0, value, 2)

def save_advice():
    top = customtkinter.CTkToplevel()
    top.title("Notificación")
    top.overrideredirect(True)
    top.w = 265
    top.h = 210
    top.geometry(f"{top.w}x{top.h}")
    top.configure(bg_color="white", fg_color="white")
    #Centrar la ventana en la pantalla
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width - top.w) // 2
    y = (screen_height - top.h) // 2
    top.geometry(f"+{x}+{y}")
    top.after(2000, top.destroy)
    gif_path = "imagenes/save_verified.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(gif.copy())
            gif.seek(len(frames))  # Mover al siguiente frame
    except EOFError:
        pass
    
    label = tk.Label(top)
    label.pack(pady=15)
    label_text = tk.Label(top, text="¡Guardado con exito!", bg="white", font=("Roboto", 15))
    label_text.pack(pady=25)
    set_opacity(top, 0.92)

    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)

def edit_advice():
    top = customtkinter.CTkToplevel()
    top.title("Notificación")
    top.overrideredirect(True)
    top.w = 265
    top.h = 210
    top.geometry(f"{top.w}x{top.h}")
    top.configure(bg_color="white", fg_color="white")
    #Centrar la ventana en la pantalla
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width - top.w) // 2
    y = (screen_height - top.h) // 2
    top.geometry(f"+{x}+{y}")
    top.after(2000, top.destroy)
    gif_path = "imagenes/edit_verified.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(gif.copy())
            gif.seek(len(frames))  # Mover al siguiente frame
    except EOFError:
        pass
    
    label = tk.Label(top)
    label.pack(pady=15)
    label_text = tk.Label(top, text="¡Editado con exito!", bg="white", font=("Roboto", 15))
    label_text.pack(pady=25)
    set_opacity(top, 0.92)

    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)

def error_advice():
    top = customtkinter.CTkToplevel()
    top.title("Notificación")
    top.overrideredirect(True)
    top.w = 265
    top.h = 210
    top.geometry(f"{top.w}x{top.h}")
    top.configure(bg_color="white", fg_color="white")
    #Centrar la ventana en la pantalla
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width - top.w) // 2
    y = (screen_height - top.h) // 2
    top.geometry(f"+{x}+{y}")
    top.after(2000, top.destroy)
    gif_path = "imagenes/error.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(gif.copy())
            gif.seek(len(frames))  # Mover al siguiente frame
    except EOFError:
        pass
    
    label = tk.Label(top)
    label.pack(pady=15)
    label_text = tk.Label(top, text="¡Ha ocurrido un error!", bg="white", font=("Roboto", 15))
    label_text.pack(pady=25)
    set_opacity(top, 0.92)
    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)

def delete_advice():
    top = customtkinter.CTkToplevel()
    top.title("Notificación")
    top.overrideredirect(True)
    top.w = 265
    top.h = 210
    top.geometry(f"{top.w}x{top.h}")
    top.configure(bg_color="white", fg_color="white")
    #Centrar la ventana en la pantalla
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width - top.w) // 2
    y = (screen_height - top.h) // 2
    top.geometry(f"+{x}+{y}")
    top.after(2000, top.destroy)
    gif_path = "imagenes/delete.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(gif.copy())
            gif.seek(len(frames))  # Mover al siguiente frame
    except EOFError:
        pass
    
    label = tk.Label(top)
    label.pack(pady=15)
    label_text = tk.Label(top, text="¡Eliminado con exito!", bg="white", font=("Roboto", 15))
    label_text.pack(pady=25)
    set_opacity(top, 0.92)

    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)


def login_correct_advice():
    top = customtkinter.CTkToplevel()
    top.title("Notificación")
    top.overrideredirect(True)
    top.w = 265
    top.h = 210
    top.geometry(f"{top.w}x{top.h}")
    top.configure(bg_color="white", fg_color="white")
    #Centrar la ventana en la pantalla
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width - top.w) // 2
    y = (screen_height - top.h) // 2
    top.geometry(f"+{x}+{y}")
    top.after(2000, top.destroy)
    gif_path = "imagenes/save_verified.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(gif.copy())
            gif.seek(len(frames))  # Mover al siguiente frame
    except EOFError:
        pass
    
    label = tk.Label(top)
    label.pack(pady=15)
    label_text = tk.Label(top, text="¡Bienvenido!", bg="white", font=("Roboto", 15))
    label_text.pack(pady=25)
    set_opacity(top, 0.92)
    
    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)

def login_wrong_advice():
    top = customtkinter.CTkToplevel()
    top.title("Notificación")
    top.overrideredirect(True)
    top.w = 265
    top.h = 210
    top.geometry(f"{top.w}x{top.h}")
    top.configure(bg_color="white", fg_color="white")
    #Centrar la ventana en la pantalla
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width - top.w) // 2
    y = (screen_height - top.h) // 2
    top.geometry(f"+{x}+{y}")
    top.after(2000, top.destroy)
    gif_path = "imagenes/error.gif"
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(gif.copy())
            gif.seek(len(frames))  # Mover al siguiente frame
    except EOFError:
        pass
    
    label = tk.Label(top)
    label.pack(pady=15)
    label_text = tk.Label(top, text="¡Datos erroneos!", bg="white", font=("Roboto", 15))
    label_text.pack(pady=25)
    set_opacity(top, 0.92)
    
    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)