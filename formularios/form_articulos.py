import tkinter as tk
from config import  COLOR_FONDO
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.ArticulosDao import consulArt, listarArticulos, ObtenerDepositos
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import datetime
from tkinter import messagebox


class FormArticulos():

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

        self.marco_articulos = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_articulos.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_articulos, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateArt = tk.Button(self.marco_articulos, text="Crear\n Articulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_articulo(permisos))
        self.buttonCreateArt.place(x=140, y=50)

        self.buttonEditArt = tk.Button(self.marco_articulos, text="Editar\n Articulo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_Articulos(permisos, self.tablaArticulos.item(self.tablaArticulos.selection())['values']))
        self.buttonEditArt.place(x=265, y=50)

        self.buttonDeleteArt = tk.Button(self.marco_articulos, text="Desactivar\n Articulo", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarArticulos(permisos))
        self.buttonDeleteArt.place(x=390, y=50)

        self.switchStatus = tk.BooleanVar(value=True)
        self.switchArtStatus = customtkinter.CTkSwitch(self.marco_articulos, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
        self.switchArtStatus.place(x=900, y=157)

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_proveedors = customtkinter.CTkLabel(self.marco_articulos, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_proveedors.place(x=65, y=155)

        self.sventrysearch_articulos = customtkinter.StringVar()
        self.entrysearch_articulos = ttk.Entry(self.marco_articulos, textvariable=self.sventrysearch_articulos, style='Modern.TEntry', width=30)
        self.entrysearch_articulos.place(x=100, y=157)
        self.entrysearch_articulos.bind('<KeyRelease>', self.update_art_content)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.ListaArticulos = consulArt(where)
        else:
            self.ListaArticulos = listarArticulos()
            self.ListaArticulos.reverse()

        self.tablaArticulos = ttk.Treeview(self.marco_articulos, column=('codprov','nom_fiscal','rif_prov','nit_prov','tipo_per','email_prov','telf_prov','dir_fiscal','dias_credito'), height=25)
        self.tablaArticulos.place(x=22, y=200)

        self.scroll = ttk.Scrollbar(self.marco_articulos, orient='vertical', command=self.tablaArticulos.yview)
        self.scroll.place(x=1104, y=200, height=526)

        self.tablaArticulos.configure(yscrollcommand=self.scroll.set)
        self.tablaArticulos.tag_configure('evenrow')

        self.tablaArticulos.heading('#0',text="ID")
        self.tablaArticulos.heading('#1',text="CodProd")
        self.tablaArticulos.heading('#2',text="Articulo")
        self.tablaArticulos.heading('#3',text="Marca")
        self.tablaArticulos.heading('#4',text="Modelo")
        self.tablaArticulos.heading('#5',text="Serial")
        self.tablaArticulos.heading('#6',text="Exist")
        self.tablaArticulos.heading('#7',text="F-Vence")
        self.tablaArticulos.heading('#8',text="Costo")
        self.tablaArticulos.heading('#9',text="Estante")
        self.tablaArticulos.heading('#10',text="Division")

        self.tablaArticulos.column("#0", width=50, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaArticulos.column("#1", width=50, stretch=False)
        self.tablaArticulos.column("#2", width=150, stretch=False)
        self.tablaArticulos.column("#3", width=100, stretch=False)
        self.tablaArticulos.column("#4", width=100, stretch=False)
        self.tablaArticulos.column("#5", width=100, stretch=False)
        self.tablaArticulos.column("#6", width=150, stretch=False)
        self.tablaArticulos.column("#7", width=100, stretch=False)
        self.tablaArticulos.column("#8", width=200, stretch=False)
        self.tablaArticulos.column("#9", width=80, stretch=False)
        self.tablaArticulos.column("#10", width=80, stretch=False)

        for p in self.ListaArticulos:
            self.tablaArticulos.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

        self.tablaArticulos.bind('<Double-1>', lambda event: self.editar_articulo(event, self.tablaArticulos.item(self.tablaArticulos.selection())['values']))

    def crear_articulo(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateArt = customtkinter.CTkToplevel()
        self.topCreateArt.title("Crear Articulos")
        self.topCreateArt.w = 800
        self.topCreateArt.h = 600
        self.topCreateArt.geometry(f"{self.topCreateArt.w}x{self.topCreateArt.h}")
        self.topCreateArt.resizable(False, False)
        self.topCreateArt.configure(bg_color='#6a717e')
        self.topCreateArt.configure(fg_color='#6a717e')
        #Centrar la ventana en la pantalla
        screen_width = self.topCreateArt.winfo_screenwidth()
        screen_height = self.topCreateArt.winfo_screenheight()
        x = (screen_width - self.topCreateArt.w) // 2
        y = (screen_height - self.topCreateArt.h) // 2
        self.topCreateArt.geometry(f"+{x}+{y}")
        self.topCreateArt.lift()
        self.topCreateArt.grab_set()
        self.topCreateArt.transient()
        #Datos para el proveedor
        marco_creararticulos = customtkinter.CTkFrame(self.topCreateArt, width=750,height=550, bg_color="white", fg_color="white")
        marco_creararticulos.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(marco_creararticulos, 0.8)
        self.lblinfo = customtkinter.CTkLabel(marco_creararticulos, text="Creacion de nuevo articulo", font=("Roboto",14))
        self.lblinfo.place(relx=0.4, rely=0.04)

        #Codigo del Producto
        self.lblcodProducto = customtkinter.CTkLabel(marco_creararticulos, text='Codigo Producto', font=("Roboto", 13))
        self.lblcodProducto.place(x=85, y=50)

        self.svcodProducto = customtkinter.StringVar()
        self.entrycodProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svcodProducto)
        self.entrycodProducto.place(x=70, y=80)
        self.entrycodProducto.configure(style='Entry.TEntry')

        #Nombre del producto
        self.lblnombProducto = customtkinter.CTkLabel(marco_creararticulos, text='Nombre del Producto', font=("Roboto", 13))
        self.lblnombProducto.place(x=230, y=50)

        self.svnombProducto = customtkinter.StringVar()
        self.entrynombProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svnombProducto)
        self.entrynombProducto.place(x=230, y=80)
        self.entrynombProducto.configure(style='Entry.TEntry')

        #Marca del producto
        self.lblmarcaProducto = customtkinter.CTkLabel(marco_creararticulos, text='Marca Producto', font=("Roboto", 13))
        self.lblmarcaProducto.place(x=405, y=50)

        self.svmarcaProducto = customtkinter.StringVar()
        self.entrymarcaProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svmarcaProducto)
        self.entrymarcaProducto.place(x=390, y=80)
        self.entrymarcaProducto.configure(style='Entry.TEntry')

        #Modelo del producto
        self.lblmodeloProducto = customtkinter.CTkLabel(marco_creararticulos, text='Modelo Producto', font=("Roboto", 13))
        self.lblmodeloProducto.place(x=565, y=50)

        self.svmodeloProducto = customtkinter.StringVar()
        self.entrymodeloProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svmodeloProducto)
        self.entrymodeloProducto.place(x=550, y=80)
        self.entrymodeloProducto.configure(style='Entry.TEntry')
        ###
        #Serial del producto
        self.lblserialProducto = customtkinter.CTkLabel(marco_creararticulos, text='Serial Producto', font=("Roboto", 13))
        self.lblserialProducto.place(x=85, y=120)

        self.svserialProducto = customtkinter.StringVar()
        self.entryserialProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svserialProducto)
        self.entryserialProducto.place(x=70, y=150)
        self.entryserialProducto.configure(style='Entry.TEntry')

        #Lote del producto
        self.lblloteProducto = customtkinter.CTkLabel(marco_creararticulos, text='Lote Producto', font=("Roboto", 13))
        self.lblloteProducto.place(x=250, y=120)

        self.svloteProducto = customtkinter.StringVar()
        self.entryloteProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svloteProducto)
        self.entryloteProducto.place(x=230, y=150)
        self.entryloteProducto.configure(style='Entry.TEntry')

        #Fecha V del producto
        self.lblfecha_vencimiento = customtkinter.CTkLabel(marco_creararticulos, text='Fecha Vencimiento', font=("Roboto", 13))
        self.lblfecha_vencimiento.place(x=395, y=120)

        self.svfecha_vencimiento = customtkinter.StringVar()
        self.entryfecha_vencimiento = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svfecha_vencimiento)
        self.entryfecha_vencimiento.place(x=390, y=150)
        self.entryfecha_vencimiento.configure(style='Entry.TEntry')

        #Seleccion de Deposito
        depositos = ObtenerDepositos()
        self.svdepositos_var = customtkinter.StringVar(value="Depositos")
        self.multioption = customtkinter.CTkOptionMenu(marco_creararticulos, values=[deposito[1] for deposito in depositos], variable=self.svdepositos_var)
        self.multioption.place(x=550, y=145)

        





