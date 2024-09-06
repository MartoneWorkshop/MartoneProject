import tkinter as tk
from config import  COLOR_FONDO
import PIL
import sqlite3
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.ProductoDao import Producto, searchProducts, listProduct, getDepots, getSupplier, getCategory, save_product, edit_product, product_inactive, productDisable
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import datetime
from tkinter import messagebox


class FormProducts():

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
        def adjustImage(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
        
        self.barra_inferior.bind("<Configure>", adjustImage)

        # Segundo Label con la imagen
        self.label_imagen = tk.Label(self.barra_inferior, image=imagen_tk)
        self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_FONDO)

        self.frame_products = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.frame_products.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.frame_products, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateArt = tk.Button(self.frame_products, text="Crear\n Producto", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormCreateProduct(permisos))
        self.buttonCreateArt.place(x=140, y=50)
        if 'ALMA1005' in permisos:
            self.buttonEditArt = tk.Button(self.frame_products, text="Editar\n Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']))
            self.buttonEditArt.place(x=265, y=50)
        else:
            self.buttonEditArt = tk.Button(self.frame_products, text="Editar\n Producto", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']))
            self.buttonEditArt.place(x=265, y=50)
            
        if 'ALMA1006' in permisos:
            self.buttonDeleteArt = tk.Button(self.frame_products, text="Desactivar\n Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.inactivateProduct(permisos))
            self.buttonDeleteArt.place(x=390, y=50)
        else:
            self.buttonDeleteArt = tk.Button(self.frame_products, text="Desactivar\n Producto", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.inactivateProduct(permisos))
            self.buttonDeleteArt.place(x=390, y=50)
        
        if 'ALMA1007' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchProStatus = customtkinter.CTkSwitch(self.frame_products, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.showStatus)
            self.switchProStatus.place(x=900, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchProStatus = customtkinter.CTkSwitch(self.frame_products, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.showStatus)
            self.switchProStatus.place(x=900, y=157)
            

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_productos = customtkinter.CTkLabel(self.frame_products, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_productos.place(x=65, y=155)

        self.sventrysearch_productos = customtkinter.StringVar()
        self.entrysearch_productos = ttk.Entry(self.frame_products, textvariable=self.sventrysearch_productos, style='Modern.TEntry', width=30)
        self.entrysearch_productos.place(x=100, y=157)
        self.entrysearch_productos.bind('<KeyRelease>', self.updateSearch)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.productList = searchProducts(where)
        else:
            self.productList = listProduct()
            self.productList.reverse()

        self.productTable = ttk.Treeview(self.frame_products, column=('codProducto','codDep','codgrupo','codProv','nombre_producto','marca','modelo','serial','costo','descripcion'), height=25)
        self.productTable.place(x=32, y=200)

        self.scroll = ttk.Scrollbar(self.frame_products, orient='vertical', command=self.productTable.yview)
        self.scroll.place(x=1084, y=200, height=526)

        self.productTable.configure(yscrollcommand=self.scroll.set)
        self.productTable.tag_configure('evenrow')

        self.productTable.heading('#0',text="ID" )
        self.productTable.heading('#1',text="CodProducto")
        self.productTable.heading('#2',text="Deposito")
        self.productTable.heading('#3',text="Categoria")
        self.productTable.heading('#4',text="Proveedor")
        self.productTable.heading('#5',text="Nomb Producto")
        self.productTable.heading('#6',text="Marca")
        self.productTable.heading('#7',text="Modelo")
        self.productTable.heading('#8',text="Serial")
        self.productTable.heading('#9',text="Costo")
        self.productTable.heading('#10',text="Descripcion")

        self.productTable.column("#0", width=50, stretch=True, anchor='w')
        self.productTable.column("#1", width=100, stretch=True)
        self.productTable.column("#2", width=100, stretch=True)
        self.productTable.column("#3", width=100, stretch=True)
        self.productTable.column("#4", width=100, stretch=True)
        self.productTable.column("#5", width=100, stretch=True)
        self.productTable.column("#6", width=100, stretch=True)
        self.productTable.column("#7", width=100, stretch=True)
        self.productTable.column("#8", width=100, stretch=True)
        self.productTable.column("#9", width=100, stretch=True)
        self.productTable.column("#10", width=100, stretch=True)

        for p in self.productList:
            self.productTable.insert('','end',iid=p[0], text=p[0],values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

        self.productTable.bind('<Double-1>', lambda event: self.FormEditProduct(event, self.productTable.item(self.productTable.selection())['values']))

    def showStatus(self):
        if self.switchStatus.get():
            self.switchProStatus.configure(text="Activos")
            self.showActive()
        else:
            self.switchProStatus.configure(text="Inactivos")
            self.showInactive()
     
    def showActive(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.productTable.delete(*self.productTable.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listProduct()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.productTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6],p[7],p[8],p[9],p[10]))

    def showInactive(self):
        self.productTable.delete(*self.productTable.get_children())
        permisos_desactivados = product_inactive()
        for p in permisos_desactivados:
            self.productTable.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

    def updateSearch(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_Productos.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM Productos WHERE
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
        for p in self.productList:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.productTable.delete(*self.productTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.productTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()
        
    def FormCreateProduct(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateArt = customtkinter.CTkToplevel()
        self.topCreateArt.title("Nuevo Producto")
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
        marco_crearproductos = customtkinter.CTkFrame(self.topCreateArt, width=550,height=550, bg_color="white", fg_color="white")
        marco_crearproductos.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(marco_crearproductos, 0.8)
        self.lblinfo = customtkinter.CTkLabel(marco_crearproductos, text="Registro de Producto", font=("Roboto",14))
        self.lblinfo.place(relx=0.36, rely=0.04)
        #LINEA 1
        #Codigo del Producto 1.1
        self.lblcodProducto = customtkinter.CTkLabel(marco_crearproductos, text='Codigo Producto', font=("Roboto", 13))
        self.lblcodProducto.place(x=55, y=60)

        self.svcodProducto = customtkinter.StringVar()
        self.entrycodProducto = ttk.Entry(marco_crearproductos, style='Modern.TEntry', textvariable=self.svcodProducto)
        self.entrycodProducto.place(x=45, y=90)
        self.entrycodProducto.configure(style='Entry.TEntry')

        #Nombre del producto 1.2
        self.lblnombProducto = customtkinter.CTkLabel(marco_crearproductos, text='Nombre del Producto', font=("Roboto", 13))
        self.lblnombProducto.place(x=202, y=60)

        self.svnombProducto = customtkinter.StringVar()
        self.entrynombProducto = ttk.Entry(marco_crearproductos, style='Modern.TEntry', textvariable=self.svnombProducto)
        self.entrynombProducto.place(x=200, y=90)
        self.entrynombProducto.configure(style='Entry.TEntry')

       #Seleccionar el proveedor del producto 1.3
        self.lblmodeloProducto = customtkinter.CTkLabel(marco_crearproductos, text='Proveedor', font=("Roboto", 13))
        self.lblmodeloProducto.place(x=365, y=60)
        
        proveedores = getSupplier()
        self.svproveedor_var = customtkinter.StringVar(value="Proveedor")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearproductos, values=[proveedor[2] for proveedor in proveedores], variable=self.svproveedor_var)
        self.multioption.place(x=360, y=85)
    
        
        ###LINEA 2
        ##Marca del producto 2.1
        self.lblmarcaProducto = customtkinter.CTkLabel(marco_crearproductos, text='Marca Producto', font=("Roboto", 13))
        self.lblmarcaProducto.place(x=50, y=130)

        self.svmarcaProducto = customtkinter.StringVar()
        self.entrymarcaProducto = ttk.Entry(marco_crearproductos, style='Modern.TEntry', textvariable=self.svmarcaProducto)
        self.entrymarcaProducto.place(x=45, y=160)
        self.entrymarcaProducto.configure(style='Entry.TEntry')
        
        ##Modelo del producto 2.2
        self.lblmodeloProducto = customtkinter.CTkLabel(marco_crearproductos, text='Modelo Producto', font=("Roboto", 13))
        self.lblmodeloProducto.place(x=200, y=130)

        self.svmodeloProducto = customtkinter.StringVar()
        self.entrymodeloProducto = ttk.Entry(marco_crearproductos, style='Modern.TEntry', textvariable=self.svmodeloProducto)
        self.entrymodeloProducto.place(x=200, y=160)
        self.entrymodeloProducto.configure(style='Entry.TEntry')
        
        #####
        ##Serial del producto 2.3
        self.lblserialProducto = customtkinter.CTkLabel(marco_crearproductos, text='Serial Producto', font=("Roboto", 13))
        self.lblserialProducto.place(x=365, y=130)

        self.svserialProducto = customtkinter.StringVar()
        self.entryserialProducto = ttk.Entry(marco_crearproductos, style='Modern.TEntry', textvariable=self.svserialProducto)
        self.entryserialProducto.place(x=360, y=160)
        self.entryserialProducto.configure(style='Entry.TEntry')

        #Linea 3
        ##Costo del producto 3.1
        self.lblcostoProducto = customtkinter.CTkLabel(marco_crearproductos, text='Costo Producto', font=("Roboto", 13))
        self.lblcostoProducto.place(x=50, y=200)
#
        self.svcostoProducto = customtkinter.StringVar()
        self.entrycostoProducto = ttk.Entry(marco_crearproductos, style='Modern.TEntry', textvariable=self.svcostoProducto)
        self.entrycostoProducto.place(x=45, y=230)
        self.entrycostoProducto.configure(style='Entry.TEntry')
#
        ###Categoria del producto 3.2
        self.lblcategoriaProducto = customtkinter.CTkLabel(marco_crearproductos, text='Categoria', font=("Roboto", 13))
        self.lblcategoriaProducto.place(x=205, y=200)
        
        categoria = getCategory() 
        self.svcategoria_var = customtkinter.StringVar(value="Categoria")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearproductos, values=[categoria[2] for categoria in categoria], variable=self.svcategoria_var)
        self.multioption.place(x=200, y=230)

        ##Seleccion de Deposito 3.3
        self.lblDepositoProducto = customtkinter.CTkLabel(marco_crearproductos, text='Deposito', font=("Roboto", 13))
        self.lblDepositoProducto.place(x=365, y=200)
    
        depositos = getDepots()
        self.svdepositos_var = customtkinter.StringVar(value="Depositos")
        self.multioption = customtkinter.CTkOptionMenu(marco_crearproductos, values=[deposito[2] for deposito in depositos], variable=self.svdepositos_var)
        
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
        
        self.lbldescripcionProd = customtkinter.CTkLabel(marco_crearproductos, text='Descripcion del Producto', font=("Roboto", 13))
        self.lbldescripcionProd.place(x=55, y=280)

        self.descripcionProd = customtkinter.CTkTextbox(marco_crearproductos, width=445, height=55, border_width=1)
        self.descripcionProd.place(x=45, y=310)

        character_count_label = customtkinter.CTkLabel(marco_crearproductos, text="")
        character_count_label.place(x=440, y=370)

        def on_text_change(event):
            validate_text(self.descripcionProd.get("1.0", "end-1c"))

        self.descripcionProd.bind("<KeyRelease>", on_text_change)
        
        self.buttonGuardarArt = tk.Button(marco_crearproductos, text="Guardar Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.GuardarProducto())
        self.buttonGuardarArt.place(x=200, y=450)

    def GuardarProducto(self):
        try:
            # Otener el contenido del Entry
            codart = buscarCorrelativo('producto')
            codart = codart + 1
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")

            productos = Producto(
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
                save_product(productos)
                actualizarCorrelativo('producto')

                self.topCreateArt.destroy()
            else:
                edit_product(productos, self.id)
                self.topEditArt.destroy()

            self.updateTable()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarProducto, form_products: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                
    def updateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.productTable.delete(*self.productTable.get_children())

            if where is not None and len(where) > 0:
                self.ListaProducto = searchProducts(where)
            else:
                self.ListaProducto = listProduct()
                self.ListaProducto.reverse()

            for p in self.ListaProducto:
                self.productTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarProductosEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            
    def FormEditProduct(self, permisos, values):
        #Creacion del top level
        if values:
            self.id = self.productTable.item(self.productTable.selection())['text']
            self.editarcodProducto = self.productTable.item(self.productTable.selection())['values'][0]
            self.editarnombProducto = self.productTable.item(self.productTable.selection())['values'][4]
            self.editarproveedor = self.productTable.item(self.productTable.selection())['values'][3]
            self.editarmarcaProducto = self.productTable.item(self.productTable.selection())['values'][5]
            self.editarmodeloProducto = self.productTable.item(self.productTable.selection())['values'][6]
            self.editarserialProducto = self.productTable.item(self.productTable.selection())['values'][7]
            self.editarcostoProducto = self.productTable.item(self.productTable.selection())['values'][8]
            self.editarcategoria_var = self.productTable.item(self.productTable.selection())['values'][2]
            self.editardepositos_var = self.productTable.item(self.productTable.selection())['values'][1]
            self.editardescripcionProd = self.productTable.item(self.productTable.selection())['values'][9]
            
            
            self.topEditArt = customtkinter.CTkToplevel()
            self.topEditArt.title("Editar Producto")
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
            marco_editarproductos = customtkinter.CTkFrame(self.topEditArt, width=550,height=550, bg_color="white", fg_color="white")
            marco_editarproductos.place(relx=0.5, rely=0.5, anchor="center")
            set_opacity(marco_editarproductos, 0.8)
            self.lblinfo = customtkinter.CTkLabel(marco_editarproductos, text="Registro de Producto", font=("Roboto",14))
            self.lblinfo.place(relx=0.36, rely=0.04)
            #LINEA 1
            #Codigo del Producto 1.1
            self.lblcodProducto = customtkinter.CTkLabel(marco_editarproductos, text='Codigo Producto', font=("Roboto", 13))
            self.lblcodProducto.place(x=55, y=60)

            self.svcodProducto = customtkinter.StringVar(value=self.editarcodProducto)
            self.entrycodProducto = ttk.Entry(marco_editarproductos, style='Modern.TEntry', textvariable=self.svcodProducto)
            self.entrycodProducto.place(x=45, y=90)
            self.entrycodProducto.configure(style='Entry.TEntry')

            #Nombre del producto 1.2
            self.lblnombProducto = customtkinter.CTkLabel(marco_editarproductos, text='Nombre del Producto', font=("Roboto", 13))
            self.lblnombProducto.place(x=202, y=60)

            self.svnombProducto = customtkinter.StringVar(value=self.editarnombProducto)
            self.entrynombProducto = ttk.Entry(marco_editarproductos, style='Modern.TEntry', textvariable=self.svnombProducto)
            self.entrynombProducto.place(x=200, y=90)
            self.entrynombProducto.configure(style='Entry.TEntry')

       #    Seleccionar el proveedor del producto 1.3
            self.lblprovProducto = customtkinter.CTkLabel(marco_editarproductos, text='Proveedor', font=("Roboto", 13))
            self.lblprovProducto.place(x=365, y=60)

            proveedores = getSupplier()
            self.svproveedor_var = customtkinter.StringVar(value=self.editarproveedor)
            self.multioption = customtkinter.CTkOptionMenu(marco_editarproductos, values=[proveedor[2] for proveedor in proveedores], variable=self.svproveedor_var)
            self.multioption.place(x=360, y=85)


            ###LINEA 2
            ##Marca del producto 2.1
            self.lblmarcaProducto = customtkinter.CTkLabel(marco_editarproductos, text='Marca Producto', font=("Roboto", 13))
            self.lblmarcaProducto.place(x=50, y=130)

            self.svmarcaProducto = customtkinter.StringVar(value=self.editarmarcaProducto)
            self.entrymarcaProducto = ttk.Entry(marco_editarproductos, style='Modern.TEntry', textvariable=self.svmarcaProducto)
            self.entrymarcaProducto.place(x=45, y=160)
            self.entrymarcaProducto.configure(style='Entry.TEntry')

            ##Modelo del producto 2.2
            self.lblmodeloProducto = customtkinter.CTkLabel(marco_editarproductos, text='Modelo Producto', font=("Roboto", 13))
            self.lblmodeloProducto.place(x=200, y=130)

            self.svmodeloProducto = customtkinter.StringVar(value=self.editarmodeloProducto)
            self.entrymodeloProducto = ttk.Entry(marco_editarproductos, style='Modern.TEntry', textvariable=self.svmodeloProducto)
            self.entrymodeloProducto.place(x=200, y=160)
            self.entrymodeloProducto.configure(style='Entry.TEntry')

            #####
            ##Serial del producto 2.3
            self.lblserialProducto = customtkinter.CTkLabel(marco_editarproductos, text='Serial Producto', font=("Roboto", 13))
            self.lblserialProducto.place(x=365, y=130)

            self.svserialProducto = customtkinter.StringVar(value=self.editarserialProducto)
            self.entryserialProducto = ttk.Entry(marco_editarproductos, style='Modern.TEntry', textvariable=self.svserialProducto)
            self.entryserialProducto.place(x=360, y=160)
            self.entryserialProducto.configure(style='Entry.TEntry')

            #Linea 3
            ##Costo del producto 3.1
            self.lblcostoProducto = customtkinter.CTkLabel(marco_editarproductos, text='Costo Producto', font=("Roboto", 13))
            self.lblcostoProducto.place(x=50, y=200)
#   
            self.svcostoProducto = customtkinter.StringVar(value=self.editarcostoProducto)
            self.entrycostoProducto = ttk.Entry(marco_editarproductos, style='Modern.TEntry', textvariable=self.svcostoProducto)
            self.entrycostoProducto.place(x=45, y=230)
            self.entrycostoProducto.configure(style='Entry.TEntry')
#   
            ###Categoria del producto 3.2
            self.lblcategoriaProducto = customtkinter.CTkLabel(marco_editarproductos, text='Categoria', font=("Roboto", 13))
            self.lblcategoriaProducto.place(x=205, y=200)

            categoria = getCategory() 
            self.svcategoria_var = customtkinter.StringVar(value=self.editarcategoria_var)
            self.multioption = customtkinter.CTkOptionMenu(marco_editarproductos, values=[categoria[3] for categoria in categoria], variable=self.svcategoria_var)
            self.multioption.place(x=200, y=230)

            ##Seleccion de Deposito 3.3
            self.lblDepositoProducto = customtkinter.CTkLabel(marco_editarproductos, text='Deposito', font=("Roboto", 13))
            self.lblDepositoProducto.place(x=365, y=200)

            depositos = getDepots()
            self.svdepositos_var = customtkinter.StringVar(value=self.editardepositos_var)
            self.multioption = customtkinter.CTkOptionMenu(marco_editarproductos, values=[deposito[2] for deposito in depositos], variable=self.svdepositos_var)

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

            self.lbldescripcionProd = customtkinter.CTkLabel(marco_editarproductos, text='Descripcion del Producto', font=("Roboto", 13))
            self.lbldescripcionProd.place(x=55, y=280)

            self.descripcionProd = customtkinter.CTkTextbox(marco_editarproductos, width=445, height=55, border_width=1)
            self.descripcionProd.place(x=45, y=310)
            self.descripcionProd.insert("1.0", self.editardescripcionProd)
            
            character_count_label = customtkinter.CTkLabel(marco_editarproductos, text="")
            character_count_label.place(x=440, y=370)

            def on_text_change(event):
                validate_text(self.descripcionProd.get("1.0", "end-1c"))

            self.descripcionProd.bind("<KeyRelease>", on_text_change)

            self.buttonActualizarArt = tk.Button(marco_editarproductos, text="Actualizar Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.GuardarProducto())
            self.buttonActualizarArt.place(x=200, y=450)

        else:
            messagebox.showerror("Error", "Debe seleccionar un modulo")

    def inactivateProduct(self, permisos):
        try:
            self.id = self.productTable.item(self.productTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este producto?")
            if confirmar:
                productDisable(self.id)
                self.updateTable()
        except Exception as e:
            error_advice()
            mensaje = f'Error en inactivateProduct, form_products: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

