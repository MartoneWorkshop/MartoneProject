import tkinter as tk
from config import  COLOR_FONDO
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.DepositosDao import Deposito, InformacionDeposito, ListarDepositos, obtener_depositos,  SaveDepot, EditDepot, DepotDisable
from config import COLOR_MENU_LATERAL
import datetime
from tkinter import messagebox


class FormDepot():

    def __init__(self, cuerpo_principal, permisos):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        ruta_imagen = "imagenes/background.png"
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_tk = imagen_tk
        # Crear el Label con la imagen de fondo
        label_fondo = tk.Label(cuerpo_principal, image=imagen_tk)
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
        
        self.barra_inferior.bind("<Configure>", ajustar_imagen)

        # Segundo Label con la imagen
        self.label_imagen = tk.Label(self.barra_inferior, image=imagen_tk)
        self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_FONDO)

        self.marco_adjustdepot = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_adjustdepot.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_adjustdepot, 0.8)
        
        self.buttonCreateDepot = tk.Button(self.marco_adjustdepot, text="Crear\n Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_deposito(permisos))
        self.buttonCreateDepot.place(x=180, y=60)

        self.buttonEditDepot = tk.Button(self.marco_adjustdepot, text="Editar\n Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_deposito(permisos, self.tablaDeposito.item(self.tablaDeposito.selection())['values']))
        self.buttonEditDepot.place(x=290, y=60)

        self.buttonDisableDepot = tk.Button(self.marco_adjustdepot, text="Desactivar\n Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.desactivarDeposito(permisos))
        self.buttonDisableDepot.place(x=395, y=60)

        where = ""
        if len(where) > 0:
            self.ListaDeposito = InformacionDeposito(where)
        else:
            self.ListaDeposito = ListarDepositos()
            self.ListaDeposito.reverse()
        self.tablaDeposito = ttk.Treeview(self.marco_adjustdepot, column=('codDep','name_dep','date_create','date_update'), height=25)
        self.tablaDeposito.place(x=180, y=140)

        self.tablaDeposito.heading('#0',text="ID")
        self.tablaDeposito.heading('#1',text="Cod Deposito")
        self.tablaDeposito.heading('#2',text="Nombre Deposito")
        self.tablaDeposito.heading('#3',text="DateCreated")
        self.tablaDeposito.heading('#4',text="DateUpdate")

        self.tablaDeposito.column("#0", width=100, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaDeposito.column("#1", width=150, stretch=False)
        self.tablaDeposito.column("#2", width=150, stretch=False)
        self.tablaDeposito.column("#3", width=150, stretch=False)
        self.tablaDeposito.column("#4", width=150, stretch=False)

        for p in self.ListaDeposito:
            self.tablaDeposito.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4]))

    def crear_deposito(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateDepot = customtkinter.CTkToplevel()
        self.topCreateDepot.title("Crear Deposito")
        self.topCreateDepot.w = 400
        self.topCreateDepot.h = 250
        self.topCreateDepot.geometry(f"{self.topCreateDepot.w}x{self.topCreateDepot.h}")
        self.topCreateDepot.resizable(False, False)
        self.topCreateDepot.configure(bg_color='#6a717e')
        self.topCreateDepot.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topCreateDepot.winfo_screenwidth()
        screen_height = self.topCreateDepot.winfo_screenheight()
        x = (screen_width - self.topCreateDepot.w) // 2
        y = (screen_height - self.topCreateDepot.h) // 2
        self.topCreateDepot.geometry(f"+{x}+{y}")

        self.topCreateDepot.lift()
        self.topCreateDepot.grab_set()
        self.topCreateDepot.transient()

        marco_createDepot = customtkinter.CTkFrame(self.topCreateDepot, width=350,height=200, bg_color="white", fg_color="white")
        marco_createDepot.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_createDepot, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_createDepot, text="Crear Deposito", font=("Roboto",13))
        self.lblinfo.place(x=133, rely=0.1)

        self.lblnombre_deposito = customtkinter.CTkLabel(marco_createDepot, text='Nombre del Deposito', font=("Roboto", 13))
        self.lblnombre_deposito.place(x=120, y=60)

        self.svnombre_deposito = customtkinter.StringVar()
        self.entrynombre_deposito = ttk.Entry(marco_createDepot, style='Modern.TEntry', textvariable=self.svnombre_deposito)
        self.entrynombre_deposito.place(x=120, y=90)
        self.entrynombre_deposito.configure(style='Entry.TEntry')

        self.buttonCrearDeposito = tk.Button(marco_createDepot, text="Crear Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarDeposito)
        self.buttonCrearDeposito.place(x=118, y=140)

        self.tablaDeposito.bind('<Double-1>', lambda event: self.editar_deposito(event, self.tablaDeposito.item(self.tablaDeposito.selection())['values']))

    def editar_deposito(self, permisos, values):
        if values:
    # Creación del top level
            self.id = self.tablaDeposito.item(self.tablaDeposito.selection())['text']
            self.nombre_deposito = self.tablaDeposito.item(self.tablaDeposito.selection())['values'][1]
            #Creacion del top level
            self.topEditDepot = customtkinter.CTkToplevel()
            self.topEditDepot.title("Crear Modulo")
            self.topEditDepot.w = 400
            self.topEditDepot.h = 250
            self.topEditDepot.geometry(f"{self.topEditDepot.w}x{self.topEditDepot.h}")
            self.topEditDepot.resizable(False, False)
            self.topEditDepot.configure(bg_color='#6a717e')
            self.topEditDepot.configure(fg_color='#6a717e')

            #Centrar la ventana en la pantalla
            screen_width = self.topEditDepot.winfo_screenwidth()
            screen_height = self.topEditDepot.winfo_screenheight()
            x = (screen_width - self.topEditDepot.w) // 2
            y = (screen_height - self.topEditDepot.h) // 2
            self.topEditDepot.geometry(f"+{x}+{y}")

            self.topEditDepot.lift()
            self.topEditDepot.grab_set()
            self.topEditDepot.transient()

            marco_EditDepot = customtkinter.CTkFrame(self.topEditDepot, width=350,height=200, bg_color="white", fg_color="white")
            marco_EditDepot.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(marco_EditDepot, 0.8)

            self.lblinfo = customtkinter.CTkLabel(marco_EditDepot, text="Editar Deposito", font=("Roboto",13))
            self.lblinfo.place(x=133, rely=0.1)

            self.lblnombre_deposito = customtkinter.CTkLabel(marco_EditDepot, text='Nombre del Deposito', font=("Roboto", 13))
            self.lblnombre_deposito.place(x=120, y=60)

            self.svnombre_deposito = customtkinter.StringVar(value=self.nombre_deposito)
            self.entrynombre_deposito = ttk.Entry(marco_EditDepot, style='Modern.TEntry', textvariable=self.svnombre_deposito)
            self.entrynombre_deposito.place(x=120, y=90)
            self.entrynombre_deposito.configure(style='Entry.TEntry')

            self.buttonEditarDeposito = tk.Button(marco_EditDepot, text="Editar Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarDeposito)
            self.buttonEditarDeposito.place(x=118, y=140)
        else:
            messagebox.showerror("Error", "Debe seleccionar un usuario")

    def desactivarDeposito(self, permisos):
        try:
            self.id = self.tablaDeposito.item(self.tablaDeposito.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas desactivar este deposito?")

            if confirmar:
                DepotDisable(self.id)
                self.listarDepositoEnTabla()

        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarDeposito, form_adjustdepot: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                

    def GuardarDeposito(self):
        codDep = buscarCorrelativo('deposito')
        codDep = codDep + 1

        fecha_actual = datetime.datetime.now()
        date_created = fecha_actual.strftime("%d/%m/%Y")
        date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
        
        deposito = Deposito(
            codDep,
            self.svnombre_deposito.get(),
            date_created,
            date_update
        )
        if self.id is None:
            SaveDepot(deposito)
            actualizarCorrelativo('deposito')
            self.topCreateDepot.destroy()
        else:
            EditDepot(deposito, self.id)
            self.topEditDepot.destroy()
        self.listarDepositoEnTabla()
        
    def listarDepositoEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaDeposito.delete(*self.tablaDeposito.get_children())

            if where is not None and len(where) > 0:
                self.listaCliente = InformacionDeposito(where)
            else:
                self.listaCliente = ListarDepositos()
                self.listaCliente.reverse()

            for p in self.listaCliente:
                self.tablaDeposito.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarDepositoEnTabla, form_depot: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')