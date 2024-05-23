import tkinter as tk
from config import  COLOR_FONDO
import customtkinter
from PIL import Image, ImageTk

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
    def update_frame(idx):
        frame = frames[idx]
        image_tk = ImageTk.PhotoImage(frame)
        label.configure(bg="white", image=image_tk)
        label.image = image_tk
        top.after(50, update_frame, (idx + 1) % len(frames))
    update_frame(0)