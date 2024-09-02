import tkinter as tk
from config import  COLOR_FONDO
import PIL
import sqlite3
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.ArticulosDao import Articulo, consulArt, listarArticulos, ObtenerDepositos, ObtenerProveedores, ObtenerGrupos, SaveArt, EditArt, articulosDesactivados, ArtDisable
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
        if 'ALMA1005' in permisos:
            self.buttonEditArt = tk.Button(self.marco_articulos, text="Editar\n Articulo", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.editar_articulo(permisos, self.tablaArticulos.item(self.tablaArticulos.selection())['values']))
            self.buttonEditArt.place(x=265, y=50)
        else:
            self.buttonEditArt = tk.Button(self.marco_articulos, text="Editar\n Articulo", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.editar_articulo(permisos, self.tablaArticulos.item(self.tablaArticulos.selection())['values']))
            self.buttonEditArt.place(x=265, y=50)
            
        if 'ALMA1006' in permisos:
            self.buttonDeleteArt = tk.Button(self.marco_articulos, text="Desactivar\n Articulo", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.desactivarArticulo(permisos))
            self.buttonDeleteArt.place(x=390, y=50)
        else:
            self.buttonDeleteArt = tk.Button(self.marco_articulos, text="Desactivar\n Articulo", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarArticulo(permisos))
            self.buttonDeleteArt.place(x=390, y=50)
        
        if 'ALMA1007' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchArtStatus = customtkinter.CTkSwitch(self.marco_articulos, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchArtStatus.place(x=900, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchArtStatus = customtkinter.CTkSwitch(self.marco_articulos, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchArtStatus.place(x=900, y=157)
            

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_articulos = customtkinter.CTkLabel(self.marco_articulos, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_articulos.place(x=65, y=155)

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

        self.tablaArticulos = ttk.Treeview(self.marco_articulos, column=('codProducto','codDep','codgrupo','codProv','nombre_producto','marca','modelo','serial','costo','descripcion'), height=25)
        self.tablaArticulos.place(x=32, y=200)

        self.scroll = ttk.Scrollbar(self.marco_articulos, orient='vertical', command=self.tablaArticulos.yview)
        self.scroll.place(x=1084, y=200, height=526)

        self.tablaArticulos.configure(yscrollcommand=self.scroll.set)
        self.tablaArticulos.tag_configure('evenrow')

        self.tablaArticulos.heading('#0',text="ID" )
        self.tablaArticulos.heading('#1',text="CodProducto")
        self.tablaArticulos.heading('#2',text="Deposito")
        self.tablaArticulos.heading('#3',text="Categoria")
        self.tablaArticulos.heading('#4',text="Proveedor")
        self.tablaArticulos.heading('#5',text="Nomb Producto")
        self.tablaArticulos.heading('#6',text="Marca")
        self.tablaArticulos.heading('#7',text="Modelo")
        self.tablaArticulos.heading('#8',text="Serial")
        self.tablaArticulos.heading('#9',text="Costo")
        self.tablaArticulos.heading('#10',text="Descripcion")

        self.tablaArticulos.column("#0", width=50, stretch=True, anchor='w')
        self.tablaArticulos.column("#1", width=100, stretch=True)
        self.tablaArticulos.column("#2", width=100, stretch=True)
        self.tablaArticulos.column("#3", width=100, stretch=True)
        self.tablaArticulos.column("#4", width=100, stretch=True)
        self.tablaArticulos.column("#5", width=100, stretch=True)
        self.tablaArticulos.column("#6", width=100, stretch=True)
        self.tablaArticulos.column("#7", width=100, stretch=True)
        self.tablaArticulos.column("#8", width=100, stretch=True)
        self.tablaArticulos.column("#9", width=100, stretch=True)
        self.tablaArticulos.column("#10", width=100, stretch=True)

        for p in self.ListaArticulos:
            self.tablaArticulos.insert('','end',iid=p[0], text=p[0],values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

        self.tablaArticulos.bind('<Double-1>', lambda event: self.editar_articulo(event, self.tablaArticulos.item(self.tablaArticulos.selection())['values']))

    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchArtStatus.configure(text="Activos")
            self.mostrarArtActivos()
        else:
            self.switchArtStatus.configure(text="Inactivos")
            self.mostrarArtDesactivados()
     
    def mostrarArtActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaArticulos.delete(*self.tablaArticulos.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listarArticulos()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaArticulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6],p[7],p[8],p[9],p[10]))

    def mostrarArtDesactivados(self):
        self.tablaArticulos.delete(*self.tablaArticulos.get_children())
        permisos_desactivados = articulosDesactivados()
        for p in permisos_desactivados:
            self.tablaArticulos.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

    def update_art_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_Articulos.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM Articulos WHERE
                        id LIKE ? OR 
                        name LIKE ? OR 
                        alias LIKE ? OR 
                        codmod LIKE ? OR 
                        date_created LIKE ? OR
                        date_update LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.ListaArticulos:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaArticulos.delete(*self.tablaArticulos.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaArticulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()
        
    def crear_articulo(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateArt = customtkinter.CTkToplevel()
        self.topCreateArt.title("Nuevo Articulo")
        self.topCreateArt.w = 600
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
        marco_creararticulos = customtkinter.CTkFrame(self.topCreateArt, width=550,height=550, bg_color="white", fg_color="white")
        marco_creararticulos.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(marco_creararticulos, 0.8)
        self.lblinfo = customtkinter.CTkLabel(marco_creararticulos, text="Registro de Producto", font=("Roboto",14))
        self.lblinfo.place(relx=0.36, rely=0.04)
        #LINEA 1
        #Codigo del Producto 1.1
        self.lblcodProducto = customtkinter.CTkLabel(marco_creararticulos, text='Codigo Producto', font=("Roboto", 13))
        self.lblcodProducto.place(x=55, y=60)

        self.svcodProducto = customtkinter.StringVar()
        self.entrycodProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svcodProducto)
        self.entrycodProducto.place(x=45, y=90)
        self.entrycodProducto.configure(style='Entry.TEntry')

        #Nombre del producto 1.2
        self.lblnombProducto = customtkinter.CTkLabel(marco_creararticulos, text='Nombre del Producto', font=("Roboto", 13))
        self.lblnombProducto.place(x=202, y=60)

        self.svnombProducto = customtkinter.StringVar()
        self.entrynombProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svnombProducto)
        self.entrynombProducto.place(x=200, y=90)
        self.entrynombProducto.configure(style='Entry.TEntry')

       #Seleccionar el proveedor del producto 1.3
        self.lblmodeloProducto = customtkinter.CTkLabel(marco_creararticulos, text='Proveedor', font=("Roboto", 13))
        self.lblmodeloProducto.place(x=365, y=60)
        
        proveedores = ObtenerProveedores()
        self.svproveedor_var = customtkinter.StringVar(value="Proveedor")
        self.multioption = customtkinter.CTkOptionMenu(marco_creararticulos, values=[proveedor[2] for proveedor in proveedores], variable=self.svproveedor_var)
        self.multioption.place(x=360, y=85)
    
        
        ###LINEA 2
        ##Marca del producto 2.1
        self.lblmarcaProducto = customtkinter.CTkLabel(marco_creararticulos, text='Marca Producto', font=("Roboto", 13))
        self.lblmarcaProducto.place(x=50, y=130)

        self.svmarcaProducto = customtkinter.StringVar()
        self.entrymarcaProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svmarcaProducto)
        self.entrymarcaProducto.place(x=45, y=160)
        self.entrymarcaProducto.configure(style='Entry.TEntry')
        
        ##Modelo del producto 2.2
        self.lblmodeloProducto = customtkinter.CTkLabel(marco_creararticulos, text='Modelo Producto', font=("Roboto", 13))
        self.lblmodeloProducto.place(x=200, y=130)

        self.svmodeloProducto = customtkinter.StringVar()
        self.entrymodeloProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svmodeloProducto)
        self.entrymodeloProducto.place(x=200, y=160)
        self.entrymodeloProducto.configure(style='Entry.TEntry')
        
        #####
        ##Serial del producto 2.3
        self.lblserialProducto = customtkinter.CTkLabel(marco_creararticulos, text='Serial Producto', font=("Roboto", 13))
        self.lblserialProducto.place(x=365, y=130)

        self.svserialProducto = customtkinter.StringVar()
        self.entryserialProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svserialProducto)
        self.entryserialProducto.place(x=360, y=160)
        self.entryserialProducto.configure(style='Entry.TEntry')

        #Linea 3
        ##Costo del producto 3.1
        self.lblcostoProducto = customtkinter.CTkLabel(marco_creararticulos, text='Costo Producto', font=("Roboto", 13))
        self.lblcostoProducto.place(x=50, y=200)
#
        self.svcostoProducto = customtkinter.StringVar()
        self.entrycostoProducto = ttk.Entry(marco_creararticulos, style='Modern.TEntry', textvariable=self.svcostoProducto)
        self.entrycostoProducto.place(x=45, y=230)
        self.entrycostoProducto.configure(style='Entry.TEntry')
#
        ###Categoria del producto 3.2
        self.lblcategoriaProducto = customtkinter.CTkLabel(marco_creararticulos, text='Categoria', font=("Roboto", 13))
        self.lblcategoriaProducto.place(x=205, y=200)
        
        categoria = ObtenerGrupos() 
        self.svcategoria_var = customtkinter.StringVar(value="Categoria")
        self.multioption = customtkinter.CTkOptionMenu(marco_creararticulos, values=[categoria[3] for categoria in categoria], variable=self.svcategoria_var)
        self.multioption.place(x=200, y=230)

        ##Seleccion de Deposito 3.3
        self.lblDepositoProducto = customtkinter.CTkLabel(marco_creararticulos, text='Deposito', font=("Roboto", 13))
        self.lblDepositoProducto.place(x=365, y=200)
    
        depositos = ObtenerDepositos()
        self.svdepositos_var = customtkinter.StringVar(value="Depositos")
        self.multioption = customtkinter.CTkOptionMenu(marco_creararticulos, values=[deposito[2] for deposito in depositos], variable=self.svdepositos_var)
        
        self.multioption.place(x=360, y=230)
        
        #Linea 4
        #Descripcion del producto 4.1
        
        def validate_text(text):
            character_count = len(text)
            remaining_characters = 140 - character_count

            if character_count <= 69:
                character_count_label.configure(text_color="black")
            elif character_count >= 140:
                character_count_label.configure(text_color="red")
            elif character_count >= 69:
                character_count_label.configure(text_color="#cc953d")
            character_count_label.configure(text=f"{character_count}/{remaining_characters}")

            if character_count > 140:
                text = text[:140]
                self.descripcionProd.delete("1.141", "end")

                self.descripcionProd.configure(state="normal")
                self.descripcionProd.delete("1.0", "end")
                self.descripcionProd.insert("1.0", text)
        
        self.lbldescripcionProd = customtkinter.CTkLabel(marco_creararticulos, text='Descripcion del Producto', font=("Roboto", 13))
        self.lbldescripcionProd.place(x=55, y=280)

        self.descripcionProd = customtkinter.CTkTextbox(marco_creararticulos, width=445, height=55, border_width=1)
        self.descripcionProd.place(x=45, y=310)

        character_count_label = customtkinter.CTkLabel(marco_creararticulos, text="")
        character_count_label.place(x=440, y=370)

        def on_text_change(event):
            validate_text(self.descripcionProd.get("1.0", "end-1c"))

        self.descripcionProd.bind("<KeyRelease>", on_text_change)
        
        self.buttonGuardarArt = tk.Button(marco_creararticulos, text="Guardar Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.GuardarProducto())
        self.buttonGuardarArt.place(x=200, y=450)

    def GuardarProducto(self):
        try:
            # Otener el contenido del Entry
            codart = buscarCorrelativo('articulo')
            codart = codart + 1
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")

            articulos = Articulo(
                self.svcodProducto.get(),
                self.svdepositos_var.get(),
                self.svcategoria_var.get(),
                self.svproveedor_var.get(),
                self.svnombProducto.get(),
                self.svmarcaProducto.get(),
                self.svmodeloProducto.get(),
                self.svserialProducto.get(),
                self.svcostoProducto.get(),
                self.descripcionProd.get("1.0", "end-1c"),
                date_created,
                date_update
            )
            
            if self.id is None:
                SaveArt(articulos)
                actualizarCorrelativo('articulo')

                self.topCreateArt.destroy()
            else:
                EditArt(articulos, self.id)
                self.topEditArt.destroy()

            self.listarArticulosEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarArticulo, form_articulos: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                
    def listarArticulosEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaArticulos.delete(*self.tablaArticulos.get_children())

            if where is not None and len(where) > 0:
                self.ListaArticulo = consulArt(where)
            else:
                self.ListaArticulo = listarArticulos()
                self.ListaArticulo.reverse()

            for p in self.ListaArticulo:
                self.tablaArticulos.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarArticulosEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            
    def editar_articulo(self, permisos, values):
        #Creacion del top level
        if values:
            self.id = self.tablaArticulos.item(self.tablaArticulos.selection())['text']
            self.editarcodProducto = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][0]
            self.editarnombProducto = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][4]
            self.editarproveedor = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][3]
            self.editarmarcaProducto = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][5]
            self.editarmodeloProducto = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][6]
            self.editarserialProducto = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][7]
            self.editarcostoProducto = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][8]
            self.editarcategoria_var = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][2]
            self.editardepositos_var = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][1]
            self.editardescripcionProd = self.tablaArticulos.item(self.tablaArticulos.selection())['values'][9]
            
            
            self.topEditArt = customtkinter.CTkToplevel()
            self.topEditArt.title("Editar Articulo")
            self.topEditArt.w = 600
            self.topEditArt.h = 600
            self.topEditArt.geometry(f"{self.topEditArt.w}x{self.topEditArt.h}")
            self.topEditArt.resizable(False, False)
            self.topEditArt.configure(bg_color='#6a717e')
            self.topEditArt.configure(fg_color='#6a717e')
            #Centrar la ventana en la pantalla
            screen_width = self.topEditArt.winfo_screenwidth()
            screen_height = self.topEditArt.winfo_screenheight()
            x = (screen_width - self.topEditArt.w) // 2
            y = (screen_height - self.topEditArt.h) // 2
            self.topEditArt.geometry(f"+{x}+{y}")
            self.topEditArt.lift()
            self.topEditArt.grab_set()
            self.topEditArt.transient()
            #Datos para el proveedor
            marco_editararticulos = customtkinter.CTkFrame(self.topEditArt, width=550,height=550, bg_color="white", fg_color="white")
            marco_editararticulos.place(relx=0.5, rely=0.5, anchor="center")
            set_opacity(marco_editararticulos, 0.8)
            self.lblinfo = customtkinter.CTkLabel(marco_editararticulos, text="Registro de Producto", font=("Roboto",14))
            self.lblinfo.place(relx=0.36, rely=0.04)
            #LINEA 1
            #Codigo del Producto 1.1
            self.lblcodProducto = customtkinter.CTkLabel(marco_editararticulos, text='Codigo Producto', font=("Roboto", 13))
            self.lblcodProducto.place(x=55, y=60)

            self.svcodProducto = customtkinter.StringVar(value=self.editarcodProducto)
            self.entrycodProducto = ttk.Entry(marco_editararticulos, style='Modern.TEntry', textvariable=self.svcodProducto)
            self.entrycodProducto.place(x=45, y=90)
            self.entrycodProducto.configure(style='Entry.TEntry')

            #Nombre del producto 1.2
            self.lblnombProducto = customtkinter.CTkLabel(marco_editararticulos, text='Nombre del Producto', font=("Roboto", 13))
            self.lblnombProducto.place(x=202, y=60)

            self.svnombProducto = customtkinter.StringVar(value=self.editarnombProducto)
            self.entrynombProducto = ttk.Entry(marco_editararticulos, style='Modern.TEntry', textvariable=self.svnombProducto)
            self.entrynombProducto.place(x=200, y=90)
            self.entrynombProducto.configure(style='Entry.TEntry')

       #    Seleccionar el proveedor del producto 1.3
            self.lblprovProducto = customtkinter.CTkLabel(marco_editararticulos, text='Proveedor', font=("Roboto", 13))
            self.lblprovProducto.place(x=365, y=60)

            proveedores = ObtenerProveedores()
            self.svproveedor_var = customtkinter.StringVar(value=self.editarproveedor)
            self.multioption = customtkinter.CTkOptionMenu(marco_editararticulos, values=[proveedor[2] for proveedor in proveedores], variable=self.svproveedor_var)
            self.multioption.place(x=360, y=85)


            ###LINEA 2
            ##Marca del producto 2.1
            self.lblmarcaProducto = customtkinter.CTkLabel(marco_editararticulos, text='Marca Producto', font=("Roboto", 13))
            self.lblmarcaProducto.place(x=50, y=130)

            self.svmarcaProducto = customtkinter.StringVar(value=self.editarmarcaProducto)
            self.entrymarcaProducto = ttk.Entry(marco_editararticulos, style='Modern.TEntry', textvariable=self.svmarcaProducto)
            self.entrymarcaProducto.place(x=45, y=160)
            self.entrymarcaProducto.configure(style='Entry.TEntry')

            ##Modelo del producto 2.2
            self.lblmodeloProducto = customtkinter.CTkLabel(marco_editararticulos, text='Modelo Producto', font=("Roboto", 13))
            self.lblmodeloProducto.place(x=200, y=130)

            self.svmodeloProducto = customtkinter.StringVar(value=self.editarmodeloProducto)
            self.entrymodeloProducto = ttk.Entry(marco_editararticulos, style='Modern.TEntry', textvariable=self.svmodeloProducto)
            self.entrymodeloProducto.place(x=200, y=160)
            self.entrymodeloProducto.configure(style='Entry.TEntry')

            #####
            ##Serial del producto 2.3
            self.lblserialProducto = customtkinter.CTkLabel(marco_editararticulos, text='Serial Producto', font=("Roboto", 13))
            self.lblserialProducto.place(x=365, y=130)

            self.svserialProducto = customtkinter.StringVar(value=self.editarserialProducto)
            self.entryserialProducto = ttk.Entry(marco_editararticulos, style='Modern.TEntry', textvariable=self.svserialProducto)
            self.entryserialProducto.place(x=360, y=160)
            self.entryserialProducto.configure(style='Entry.TEntry')

            #Linea 3
            ##Costo del producto 3.1
            self.lblcostoProducto = customtkinter.CTkLabel(marco_editararticulos, text='Costo Producto', font=("Roboto", 13))
            self.lblcostoProducto.place(x=50, y=200)
#   
            self.svcostoProducto = customtkinter.StringVar(value=self.editarcostoProducto)
            self.entrycostoProducto = ttk.Entry(marco_editararticulos, style='Modern.TEntry', textvariable=self.svcostoProducto)
            self.entrycostoProducto.place(x=45, y=230)
            self.entrycostoProducto.configure(style='Entry.TEntry')
#   
            ###Categoria del producto 3.2
            self.lblcategoriaProducto = customtkinter.CTkLabel(marco_editararticulos, text='Categoria', font=("Roboto", 13))
            self.lblcategoriaProducto.place(x=205, y=200)

            categoria = ObtenerGrupos() 
            self.svcategoria_var = customtkinter.StringVar(value=self.editarcategoria_var)
            self.multioption = customtkinter.CTkOptionMenu(marco_editararticulos, values=[categoria[3] for categoria in categoria], variable=self.svcategoria_var)
            self.multioption.place(x=200, y=230)

            ##Seleccion de Deposito 3.3
            self.lblDepositoProducto = customtkinter.CTkLabel(marco_editararticulos, text='Deposito', font=("Roboto", 13))
            self.lblDepositoProducto.place(x=365, y=200)

            depositos = ObtenerDepositos()
            self.svdepositos_var = customtkinter.StringVar(value=self.editardepositos_var)
            self.multioption = customtkinter.CTkOptionMenu(marco_editararticulos, values=[deposito[2] for deposito in depositos], variable=self.svdepositos_var)

            self.multioption.place(x=360, y=230)

            #Linea 4
            #Descripcion del producto 4.1

            def validate_text(text):
                character_count = len(text)
                remaining_characters = 140 - character_count

                if character_count <= 69:
                    character_count_label.configure(text_color="black")
                elif character_count >= 140:
                    character_count_label.configure(text_color="red")
                elif character_count >= 69:
                    character_count_label.configure(text_color="#cc953d")
                character_count_label.configure(text=f"{character_count}/{remaining_characters}")

                if character_count > 140:
                    text = text[:140]
                    self.descripcionProd.delete("1.141", "end")

                    self.descripcionProd.configure(state="normal")
                    self.descripcionProd.delete("1.0", "end")
                    self.descripcionProd.insert("1.0", text)

            self.lbldescripcionProd = customtkinter.CTkLabel(marco_editararticulos, text='Descripcion del Producto', font=("Roboto", 13))
            self.lbldescripcionProd.place(x=55, y=280)

            self.descripcionProd = customtkinter.CTkTextbox(marco_editararticulos, width=445, height=55, border_width=1)
            self.descripcionProd.place(x=45, y=310)
            self.descripcionProd.insert("1.0", self.editardescripcionProd)
            
            character_count_label = customtkinter.CTkLabel(marco_editararticulos, text="")
            character_count_label.place(x=440, y=370)

            def on_text_change(event):
                validate_text(self.descripcionProd.get("1.0", "end-1c"))

            self.descripcionProd.bind("<KeyRelease>", on_text_change)

            self.buttonActualizarArt = tk.Button(marco_editararticulos, text="Actualizar Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.GuardarProducto())
            self.buttonActualizarArt.place(x=200, y=450)

        else:
            messagebox.showerror("Error", "Debe seleccionar un modulo")

    def desactivarArticulo(self, permisos):
        try:
            self.id = self.tablaArticulos.item(self.tablaArticulos.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este articulo?")
            if confirmar:
                ArtDisable(self.id)
                self.listarArticulosEnTabla()
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarArticulo, form_articulos: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

