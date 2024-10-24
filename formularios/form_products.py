import tkinter as tk
from config import  COLOR_FONDO
import PIL
import sqlite3
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_ventana import loadBackgroundImage, set_opacity, set_window_icon, centerWindow
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.ProductDao import product, getDepots, searchProducts, listProduct, recoverProduct, getSupplier, getCategory, save_product, edit_product, product_inactive, productDisable
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import datetime
from tkinter import messagebox
from util.widgets import Button, Switch, SearchBar, Table

class FormProducts():

    def __init__(self, cuerpo_principal, permisos):
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.cuerpo_principal = tk.Frame(cuerpo_principal)
        self.cuerpo_principal.pack(side=tk.BOTTOM, fill='both', expand=True)  

        loadBackgroundImage(self)

        self.frame_products = customtkinter.CTkFrame(cuerpo_principal, 
                                                     width=1120,
                                                     height=800, 
                                                     bg_color="white", 
                                                     fg_color="white")
        
        self.frame_products.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.frame_products, 0.94)

        self.buttonNewProduct = Button(self.frame_products, 
                                       text="Nuevo\nProducto",
                                       command=lambda: self.FormCreateProduct(permisos),
                                       x=140,y=50)

        
        if 'ALMA1005' in permisos:
            self.buttonEditProduct = Button(self.frame_products, text="Editar\nProducto",
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']),
                                            x=265, y=50)
        else:
            self.buttonEditProduct = Button(self.frame_products, text="Editar\nProducto",
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']),
                                            state='disabled',
                                            x=265, y=50)
            
        if 'ALMA1006' in permisos:
            self.buttonDeleteProduct = Button(self.frame_products, text="Desactivar\nProducto",
                                              command=lambda: self.inactivateProduct(permisos),
                                              x=390, y=50)
        else:
            self.buttonDeleteProduct = Button(self.frame_products, text="Desactivar\nProducto",
                                              command=lambda: self.inactivateProduct(permisos),
                                              state='disabled',
                                              x=390, y=50)
        
        if 'ALMA1007' in permisos:
            self.switchStatus = Switch(self.frame_products,
                                       variable=True,
                                       command=lambda: self.showStatus(permisos),
                                       x=900, y=157)
        else:
            self.switchStatus = Switch(self.frame_products,
                                       variable=True,
                                       command=lambda: self.showStatus(permisos),
                                       state='disabled',
                                       x=900, y=157)
                
        self.productList = listProduct()
        self.productList.reverse()
        headers_product = ['CodProudcto', 'Deposito', 'Categoria', 'Nomb Producto', 
                           'Marca', 'Modelo', 'Serial', 'Costo', 'Descripcion']
        self.productTable = Table(self.frame_products, 
                                  headers=headers_product, 
                                  data_list=self.productList, 
                                  edit_command=self.FormEditProduct)
        
        self.search_bar = SearchBar(self.frame_products,
                            icon_path="imagenes/icons/search.png",
                            x=65, y=155,
                            db_table='product',
                            search_fields=['codProducto', 'nombre_producto', 'marca'],
                            dataList=self.productList,
                            dataTable=self.productTable)

    def showStatus(self, permisos):
        if self.switchStatus.switch.get():
            self.switchStatus.switch.configure(text="Activos")
            self.showActive(permisos)
        else:
            self.switchStatus.switch.configure(text="Inactivos")
            self.showInactive(permisos) 
     
    def showActive(self, permisos):
        self.buttonNewProduct = Button(self.frame_products, 
                                       text="Nuevo\nProducto",
                                       command=lambda: self.FormCreateProduct(permisos),
                                       x=140,y=50)
        if 'ALMA1008' in permisos:
            self.buttonEditProduct = Button(self.frame_products, text="Editar\nProducto",
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']),
                                            x=265, y=50)
        else: 
            self.buttonEditProduct = Button(self.frame_products, text="Editar\nProducto",
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']),
                                            state='disabled',
                                            x=265, y=50)
        if 'ALMA1010' in permisos:
            self.buttonDeleteProduct = Button(self.frame_products, text="Desactivar\nProducto",
                                              command=lambda: self.inactivateProduct(permisos),
                                              x=390, y=50)
        else:
            self.buttonDeleteProduct = Button(self.frame_products, text="Desactivar\nProducto",
                                              command=lambda: self.inactivateProduct(permisos),
                                              state='disabled',
                                              x=390, y=50)
        # Borrar los elementos existentes en la tabla de permisos
        self.productTable.delete(*self.productTable.get_children())
        # Obtener la lista de permisos activos
        active_product = listProduct()
        # Insertar los permisos activos en la tabla
        for p in active_product:
            self.productTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6],p[7],p[8],p[9],p[10]))

    def showInactive(self, permisos):
        if 'ALMA1012' in permisos:
            self.buttonNewProduct = Button(self.frame_products, 
                                       text="Restaurar\nProducto",
                                       command=lambda: self.FormCreateProduct(permisos),
                                       x=140,y=50)
        else:
            self.buttonNewProduct = Button(self.frame_products, 
                                       text="Restaurar\nProducto",
                                       command=lambda: self.FormCreateProduct(permisos),
                                       x=140,y=50)
        if 'ALMA1005' in permisos:
            self.buttonEditProduct = Button(self.frame_products, text="Editar\nProducto",
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']),
                                            state='disabled',
                                            x=265, y=50)
        else: 
            self.buttonEditProduct = Button(self.frame_products, text="Editar\nProducto",
                                            command=lambda: self.FormEditProduct(permisos, self.productTable.item(self.productTable.selection())['values']),
                                            state='disabled',
                                            x=265, y=50)
        if 'ALMA1006' in permisos:
            self.buttonDeleteProduct = Button(self.frame_products, text="Desactivar\nProducto",
                                              command=lambda: self.inactivateProduct(permisos),
                                              state='disabled',
                                              x=390, y=50)
        else:
            self.buttonDeleteProduct = Button(self.frame_products, text="Desactivar\nProducto",
                                              command=lambda: self.inactivateProduct(permisos),
                                              state='disabled',
                                              x=390, y=50)


        self.productTable.delete(*self.productTable.get_children())
        permisos_desactivados = product_inactive()
        for p in permisos_desactivados:
            self.productTable.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

    def restoreProduct(self, permisos):
        try:
            self.id = self.productTable.item(self.productTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas restaurar este producto?")

            if confirmar:
                recoverProduct(self.id)
                self.switchStatus.select(True)
                self.showStatus(permisos)
                self.updateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en restoreProduct, form_products: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
             
    def updateSearch(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.search_bar.get_se()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM product WHERE
                        id LIKE ? OR 
                        codProducto LIKE ? OR 
                        codDep LIKE ? OR 
                        id_cat LIKE ? OR
                        nombre_producto LIKE ? OR
                        marca LIKE ? OR
                        modelo LIKE ? OR
                        serial LIKE ? OR
                        costo LIKE ? OR
                        descripcion LIKE ? OR
                        created_at LIKE ? OR
                        updated_at LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content + '%',
                        '%' + self.content + '%',
                        '%' + self.content + '%',
                        '%' + self.content + '%',
                        '%' + self.content + '%',
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.productList:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower() or self.content.lower() in str(p[7]).lower() or self.content.lower() in str(p[8]).lower() or self.content.lower() in str(p[9]).lower() or self.content.lower() in str(p[10]).lower()or self.content.lower() in str(p[11]).lower()or self.content.lower() in str(p[12]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.productTable.delete(*self.productTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.productTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6], p[7], p[8], p[9], p[10]))
        self.cursor.close()
        self.connection.close()
        
    def FormCreateProduct(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateProduct = tk.Toplevel()
        self.topCreateProduct.title("Nuevo Producto")
        self.topCreateProduct.w = 600
        self.topCreateProduct.h = 600
        self.topCreateProduct.geometry(f"{self.topCreateProduct.w}x{self.topCreateProduct.h}")
        self.topCreateProduct.resizable(False, False)
        self.topCreateProduct.configure(background='#6a717e')
        #self.topCreateProduct.configure(fg_color='#6a717e')
        #Centrar la ventana en la pantalla
        centerWindow(self.topCreateProduct)
        set_window_icon(self.topCreateProduct)
        self.topCreateProduct.lift()
        self.topCreateProduct.grab_set()
        self.topCreateProduct.transient()
        #Datos para el proveedor
        frame_createProduct = customtkinter.CTkFrame(self.topCreateProduct, width=550,height=550, bg_color="white", fg_color="white")
        frame_createProduct.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(frame_createProduct, 0.8)
        self.lblinfo = customtkinter.CTkLabel(frame_createProduct, text="Registro de Producto", font=("Roboto",14))
        self.lblinfo.place(relx=0.36, rely=0.04)
        #LINEA 1
        #Codigo del Producto 1.1
        self.lblcodProducto = customtkinter.CTkLabel(frame_createProduct, text='Codigo Producto', font=("Roboto", 13))
        self.lblcodProducto.place(x=55, y=60)

        self.svcodProducto = customtkinter.StringVar()
        self.entrycodProducto = ttk.Entry(frame_createProduct, style='Modern.TEntry', textvariable=self.svcodProducto)
        self.entrycodProducto.place(x=45, y=90)
        self.entrycodProducto.configure(style='Entry.TEntry')

        #Nombre del producto 1.2
        self.lblnombProducto = customtkinter.CTkLabel(frame_createProduct, text='Nombre del Producto', font=("Roboto", 13))
        self.lblnombProducto.place(x=202, y=60)

        self.svnombProducto = customtkinter.StringVar()
        self.entrynombProducto = ttk.Entry(frame_createProduct, style='Modern.TEntry', textvariable=self.svnombProducto)
        self.entrynombProducto.place(x=200, y=90)
        self.entrynombProducto.configure(style='Entry.TEntry')

       #Seleccionar el proveedor del producto 1.3
        self.lblnombProveedor = customtkinter.CTkLabel(frame_createProduct, text='Proveedor', font=("Roboto", 13))
        self.lblnombProveedor.place(x=365, y=60)
        
        proveedores = getSupplier()
        self.svproveedor_var = customtkinter.StringVar(value="Proveedor")
        self.multioption = customtkinter.CTkOptionMenu(frame_createProduct, values=[proveedor[2] for proveedor in proveedores], variable=self.svproveedor_var)
        self.multioption.place(x=360, y=85)
    
        
        ###LINEA 2
        ##Marca del producto 2.1
        self.lblmarcaProducto = customtkinter.CTkLabel(frame_createProduct, text='Marca Producto', font=("Roboto", 13))
        self.lblmarcaProducto.place(x=50, y=130)

        self.svmarcaProducto = customtkinter.StringVar()
        self.entrymarcaProducto = ttk.Entry(frame_createProduct, style='Modern.TEntry', textvariable=self.svmarcaProducto)
        self.entrymarcaProducto.place(x=45, y=160)
        self.entrymarcaProducto.configure(style='Entry.TEntry')
        
        ##Modelo del producto 2.2
        self.lblmodeloProducto = customtkinter.CTkLabel(frame_createProduct, text='Modelo Producto', font=("Roboto", 13))
        self.lblmodeloProducto.place(x=200, y=130)

        self.svmodeloProducto = customtkinter.StringVar()
        self.entrymodeloProducto = ttk.Entry(frame_createProduct, style='Modern.TEntry', textvariable=self.svmodeloProducto)
        self.entrymodeloProducto.place(x=200, y=160)
        self.entrymodeloProducto.configure(style='Entry.TEntry')
        
        #####
        ##Serial del producto 2.3
        self.lblserialProducto = customtkinter.CTkLabel(frame_createProduct, text='Serial Producto', font=("Roboto", 13))
        self.lblserialProducto.place(x=365, y=130)

        self.svserialProducto = customtkinter.StringVar()
        self.entryserialProducto = ttk.Entry(frame_createProduct, style='Modern.TEntry', textvariable=self.svserialProducto)
        self.entryserialProducto.place(x=360, y=160)
        self.entryserialProducto.configure(style='Entry.TEntry')

        #Linea 3
        ##Costo del producto 3.1
        self.lblcostoProducto = customtkinter.CTkLabel(frame_createProduct, text='Costo Producto', font=("Roboto", 13))
        self.lblcostoProducto.place(x=50, y=200)
#
        self.svcostoProducto = customtkinter.StringVar()
        self.entrycostoProducto = ttk.Entry(frame_createProduct, style='Modern.TEntry', textvariable=self.svcostoProducto)
        self.entrycostoProducto.place(x=45, y=230)
        self.entrycostoProducto.configure(style='Entry.TEntry')
#
        ###Categoria del producto 3.2
        self.lblcategoriaProducto = customtkinter.CTkLabel(frame_createProduct, text='Categoria', font=("Roboto", 13))
        self.lblcategoriaProducto.place(x=205, y=200)
        
        categoria = getCategory() 
        self.svcategoria_var = customtkinter.StringVar(value="Categoria")
        self.multioptioncat = customtkinter.CTkOptionMenu(frame_createProduct, values=[categoria[1] for categoria in categoria], variable=self.svcategoria_var)
        self.multioptioncat.place(x=200, y=230)

        ##Seleccion de Deposito 3.3
        self.lblDepositoProducto = customtkinter.CTkLabel(frame_createProduct, text='Deposito', font=("Roboto", 13))
        self.lblDepositoProducto.place(x=365, y=200)
    
        depositos = getDepots()
        self.svdepositos_var = customtkinter.StringVar(value="Depositos")
        self.multioptiondep = customtkinter.CTkOptionMenu(frame_createProduct, values=[deposito[2] for deposito in depositos], variable=self.svdepositos_var)
        
        self.multioptiondep.place(x=360, y=230)
        
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
        
        self.lbldescripcionProd = customtkinter.CTkLabel(frame_createProduct, text='Descripcion del Producto', font=("Roboto", 13))
        self.lbldescripcionProd.place(x=55, y=280)

        self.descripcionProd = customtkinter.CTkTextbox(frame_createProduct, width=445, height=55, border_width=1)
        self.descripcionProd.place(x=45, y=310)

        character_count_label = customtkinter.CTkLabel(frame_createProduct, text="")
        character_count_label.place(x=440, y=370)

        def on_text_change(event):
            validate_text(self.descripcionProd.get("1.0", "end-1c"))

        self.descripcionProd.bind("<KeyRelease>", on_text_change)
        
        #self.buttonGuardarArt = tk.Button(frame_createProduct, text="Guardar Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
        #                                    command=lambda: self.GuardarProducto())
        #self.buttonGuardarArt.place(x=200, y=450)

        self.buttonSaveProduct = customtkinter.CTkButton(frame_createProduct, text="Guardar\nProducto",width=80, height=60, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E",text_color="white", corner_radius=7, command=lambda: self.GuardarProducto())
        self.buttonSaveProduct.place(x=250, y=450)

    def GuardarProducto(self):
        try:
            # Otener el contenido del Entry
            codpdt = buscarCorrelativo('producto')
            codpdt = codpdt + 1
            fecha_actual = datetime.datetime.now()
            created_at = fecha_actual.strftime("%Y-%m-%d")
            updated_at = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

            producto = product(
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
                created_at,
                updated_at,
                deleted_at = 'NULL'
            )
            if self.id is None:
                save_product(producto)
                actualizarCorrelativo('producto')
                self.topCreateProduct.destroy()
            else:
                edit_product(producto, self.id)
                self.topEditProduct.destroy()

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
            
            
            self.topEditProduct = tk.Toplevel()
            self.topEditProduct.title("Editar Producto")
            self.topEditProduct.w = 600
            self.topEditProduct.h = 600
            self.topEditProduct.geometry(f"{self.topEditProduct.w}x{self.topEditProduct.h}")
            self.topEditProduct.resizable(False, False)
            self.topEditProduct.configure(background='#6a717e')
            #Centrar la ventana en la pantalla
            centerWindow(self.topEditProduct)
            set_window_icon(self.topEditProduct)
            self.topEditProduct.lift()
            self.topEditProduct.grab_set()
            self.topEditProduct.transient()
            #Datos para el proveedor
            frame_editProducts = customtkinter.CTkFrame(self.topEditProduct, width=550,height=550, bg_color="white", fg_color="white")
            frame_editProducts.place(relx=0.5, rely=0.5, anchor="center")
            set_opacity(frame_editProducts, 0.8)
            self.lblinfo = customtkinter.CTkLabel(frame_editProducts, text="Registro de Producto", font=("Roboto",14))
            self.lblinfo.place(relx=0.36, rely=0.04)
            #LINEA 1
            #Codigo del Producto 1.1
            self.lblcodProducto = customtkinter.CTkLabel(frame_editProducts, text='Codigo Producto', font=("Roboto", 13))
            self.lblcodProducto.place(x=55, y=60)

            self.svcodProducto = customtkinter.StringVar(value=self.editarcodProducto)
            self.entrycodProducto = ttk.Entry(frame_editProducts, style='Modern.TEntry', textvariable=self.svcodProducto)
            self.entrycodProducto.place(x=45, y=90)
            self.entrycodProducto.configure(style='Entry.TEntry')

            #Nombre del producto 1.2
            self.lblnombProducto = customtkinter.CTkLabel(frame_editProducts, text='Nombre del Producto', font=("Roboto", 13))
            self.lblnombProducto.place(x=202, y=60)

            self.svnombProducto = customtkinter.StringVar(value=self.editarnombProducto)
            self.entrynombProducto = ttk.Entry(frame_editProducts, style='Modern.TEntry', textvariable=self.svnombProducto)
            self.entrynombProducto.place(x=200, y=90)
            self.entrynombProducto.configure(style='Entry.TEntry')

       #    Seleccionar el proveedor del producto 1.3
            self.lblprovProducto = customtkinter.CTkLabel(frame_editProducts, text='Proveedor', font=("Roboto", 13))
            self.lblprovProducto.place(x=365, y=60)

            proveedores = getSupplier()
            self.svproveedor_var = customtkinter.StringVar(value=self.editarproveedor)
            self.multioption = customtkinter.CTkOptionMenu(frame_editProducts, values=[proveedor[2] for proveedor in proveedores], variable=self.svproveedor_var)
            self.multioption.place(x=360, y=85)
            
            ###LINEA 2
            ##Marca del producto 2.1
            self.lblmarcaProducto = customtkinter.CTkLabel(frame_editProducts, text='Marca Producto', font=("Roboto", 13))
            self.lblmarcaProducto.place(x=50, y=130)

            self.svmarcaProducto = customtkinter.StringVar(value=self.editarmarcaProducto)
            self.entrymarcaProducto = ttk.Entry(frame_editProducts, style='Modern.TEntry', textvariable=self.svmarcaProducto)
            self.entrymarcaProducto.place(x=45, y=160)
            self.entrymarcaProducto.configure(style='Entry.TEntry')

            ##Modelo del producto 2.2
            self.lblmodeloProducto = customtkinter.CTkLabel(frame_editProducts, text='Modelo Producto', font=("Roboto", 13))
            self.lblmodeloProducto.place(x=200, y=130)

            self.svmodeloProducto = customtkinter.StringVar(value=self.editarmodeloProducto)
            self.entrymodeloProducto = ttk.Entry(frame_editProducts, style='Modern.TEntry', textvariable=self.svmodeloProducto)
            self.entrymodeloProducto.place(x=200, y=160)
            self.entrymodeloProducto.configure(style='Entry.TEntry')

            #####
            ##Serial del producto 2.3
            self.lblserialProducto = customtkinter.CTkLabel(frame_editProducts, text='Serial Producto', font=("Roboto", 13))
            self.lblserialProducto.place(x=365, y=130)

            self.svserialProducto = customtkinter.StringVar(value=self.editarserialProducto)
            self.entryserialProducto = ttk.Entry(frame_editProducts, style='Modern.TEntry', textvariable=self.svserialProducto)
            self.entryserialProducto.place(x=360, y=160)
            self.entryserialProducto.configure(style='Entry.TEntry')

            #Linea 3
            ##Costo del producto 3.1
            self.lblcostoProducto = customtkinter.CTkLabel(frame_editProducts, text='Costo Producto', font=("Roboto", 13))
            self.lblcostoProducto.place(x=50, y=200)
#   a
            self.svcostoProducto = customtkinter.StringVar(value=self.editarcostoProducto)
            self.entrycostoProducto = ttk.Entry(frame_editProducts, style='Modern.TEntry', textvariable=self.svcostoProducto)
            self.entrycostoProducto.place(x=45, y=230)
            self.entrycostoProducto.configure(style='Entry.TEntry')
#   
            ###Categoria del producto 3.2
            self.lblcategoriaProducto = customtkinter.CTkLabel(frame_editProducts, text='Categoria', font=("Roboto", 13))
            self.lblcategoriaProducto.place(x=205, y=200)

            categoria = getCategory() 
            self.svcategoria_var = customtkinter.StringVar(value=self.editarcategoria_var)
            self.multioption = customtkinter.CTkOptionMenu(frame_editProducts, values=[categoria[1] for categoria in categoria], variable=self.svcategoria_var)
            self.multioption.place(x=200, y=230)

            ##Seleccion de Deposito 3.3
            self.lblDepositoProducto = customtkinter.CTkLabel(frame_editProducts, text='Deposito', font=("Roboto", 13))
            self.lblDepositoProducto.place(x=365, y=200)

            depositos = getDepots()
            self.svdepositos_var = customtkinter.StringVar(value=self.editardepositos_var)
            self.multioption = customtkinter.CTkOptionMenu(frame_editProducts, values=[deposito[2] for deposito in depositos], variable=self.svdepositos_var)

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

            self.lbldescripcionProd = customtkinter.CTkLabel(frame_editProducts, text='Descripcion del Producto', font=("Roboto", 13))
            self.lbldescripcionProd.place(x=55, y=280)

            self.descripcionProd = customtkinter.CTkTextbox(frame_editProducts, width=445, height=55, border_width=1)
            self.descripcionProd.place(x=45, y=310)
            self.descripcionProd.insert("1.0", self.editardescripcionProd)
            
            character_count_label = customtkinter.CTkLabel(frame_editProducts, text="")
            character_count_label.place(x=440, y=370)

            def on_text_change(event):
                validate_text(self.descripcionProd.get("1.0", "end-1c"))

            self.descripcionProd.bind("<KeyRelease>", on_text_change)

            #self.buttonActualizarArt = tk.Button(frame_editProducts, text="Actualizar Producto", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
            #                                    command=lambda: self.GuardarProducto())
            #self.buttonActualizarArt.place(x=200, y=450)

            self.buttonActProduct = customtkinter.CTkButton(frame_editProducts, text="Actualizar\nProducto",width=80, height=60, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E",text_color="white", corner_radius=7, command=lambda: self.GuardarProducto())
            self.buttonActProduct.place(x=225, y=450)

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


