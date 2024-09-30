import tkinter as tk
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_ventana import set_window_icon, centerWindow
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.CategoryDao import category, save_cat, edit_cat, searchCategories, listCategory, catDisable, inactive_cat, recoverCategory
from config import COLOR_MENU_LATERAL
import datetime
from tkinter import messagebox
import sqlite3


class FormCategory():

    def __init__(self, cuerpo_principal, permisos):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        ruta_imagen = "imagenes/bg1.jpeg"
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

        self.frame_category = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.frame_category.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.frame_category, 0.8)
        
        self.buttonCreateCategory = tk.Button(self.frame_category, text="Crear\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.FormCreateCategory(permisos))
        self.buttonCreateCategory.place(x=260, y=60)
        if 'ALMA1004' in permisos:
            self.buttonEditCategory = tk.Button(self.frame_category, text="Editar\n Categoria", state='normal', font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.FormEditCategory(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
            self.buttonEditCategory.place(x=375, y=60)
        else:
            self.buttonEditCategory = tk.Button(self.frame_category, text="Editar\n Categoria", state="disabled", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.FormEditCategory(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
            self.buttonEditCategory.place(x=375, y=60)
        if 'ALMA1013' in permisos:
            self.buttonDisableCategory = tk.Button(self.frame_category, text="Desactivar\n Categoria", state="normal", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.categoryDisable(permisos))
            self.buttonDisableCategory.place(x=490, y=60)
        else:
            self.buttonDisableCategory = tk.Button(self.frame_category, text="Desactivar\n Categoria", state="disabled", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.categoryDisable(permisos))
            self.buttonDisableCategory.place(x=490, y=60)

        
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_categoria = customtkinter.CTkLabel(self.frame_category, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_categoria.place(x=240, y=155)

        self.sventrysearch_categoria = customtkinter.StringVar()
        self.entrysearch_categoria = ttk.Entry(self.frame_category, textvariable=self.sventrysearch_categoria, style='Modern.TEntry', width=30)
        self.entrysearch_categoria.place(x=290, y=157)
        self.entrysearch_categoria.bind('<KeyRelease>', self.updateSearch)

        if 'ALMA1015' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchStatus = customtkinter.CTkSwitch(self.frame_category, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=lambda: self.showStatus(permisos))
            self.switchStatus.place(x=720, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchStatus = customtkinter.CTkSwitch(self.frame_category, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=lambda: self.showStatus(permisos))
            self.switchStatus.place(x=720, y=157)

        #################################################### INFORMACION DE LA TABLA ####################################################
        
        where = ""
        if len(where) > 0:
            self.listCategory = searchCategories(where)
        else:
            self.listCategory = listCategory()
            self.listCategory.reverse()

        self.categoryTable = ttk.Treeview(self.frame_category, column=('name_Category','created_at','updated_at'), height=25)
        self.categoryTable.place(x=235, y=200)

        self.scroll = ttk.Scrollbar(self.frame_category, orient='vertical', command=self.categoryTable.yview)
        self.scroll.place(x=788, y=200, height=526)

        self.categoryTable.configure(yscrollcommand=self.scroll.set)
        self.categoryTable.tag_configure('evenrow')

        self.categoryTable.heading('#0',text="ID")
        self.categoryTable.heading('#1',text="Nombre Categoria")
        self.categoryTable.heading('#2',text="Date-Created")
        self.categoryTable.heading('#3',text="Date-Update")

        self.categoryTable.column("#0", width=65, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.categoryTable.column("#1", width=162, stretch=False)
        self.categoryTable.column("#2", width=162, stretch=False)
        self.categoryTable.column("#3", width=161, stretch=False)

# Crear el estilo personalizado
        style = ttk.Style()
        # Cambiar el fondo y el color de texto de las filas
        style.configure("Treeview", 
                        background="white",
                        foreground="black",
                        relief="flat",
                        rowheight=32,   # Altura de cada fila
                        fieldbackground="white")

        # Cambiar el fondo de las filas seleccionadas
        style.map("Treeview", 
                  background=[("selected", "#347083")],  # Color de la fila seleccionada
                  foreground=[("selected", "white")])    # Texto de la fila seleccionada
        
        def sort_column(tree, col, reverse):
            # Si es la columna #0 (ID), utiliza el valor de 'text'
            if col == '#0':
                data_list = [(tree.item(child, 'text'), child) for child in tree.get_children('')]
            else:
                # Para las otras columnas, usa 'set' para obtener el valor
                data_list = [(tree.set(child, col), child) for child in tree.get_children('')]

            # Ordenar la lista (en orden ascendente o descendente)
            data_list.sort(reverse=reverse)

            # Reordenar los elementos en el Treeview
            for index, (val, child) in enumerate(data_list):
                tree.move(child, '', index)

            # Actualizar el encabezado para invertir la ordenación en el próximo clic
            tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

        # Configurar los encabezados para poder hacer clic y ordenar las columnas
        for col in ('#0', '#1', '#2', '#3'):
            self.categoryTable.heading(col, command=lambda _col=col: sort_column(self.categoryTable, _col, False))

        # Alternancia de colores en las filas
        self.categoryTable.tag_configure('even', background='#DFDFDF')  # Estilo para filas pares
        self.categoryTable.tag_configure('odd', background='#E8E8E8')   # Estilo para filas impares

        for i, p in enumerate(self.listCategory):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.categoryTable.insert('',0,text=p[0], values=(p[1],p[2],p[3]), tags=(tag,))
        self.categoryTable.bind('<Double-1>', lambda event: self.FormEditCategory(event, self.categoryTable.item(self.categoryTable.selection())['values']))

    def showStatus(self, permisos):
        if self.switchStatus.get() == True:
            self.switchStatus.configure(text="Activos")
            self.showActive(permisos)
        else:
            self.switchStatus.configure(text="Inactivos")
            self.showInactive(permisos)

    def showActive(self, permisos):
        self.buttonCreateCategory = customtkinter.CTkButton(self.frame_category, text="Nuevo\nCategoria", width=80, height=60, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.FormNewDepot(permisos))
        self.buttonCreateCategory.place(x=260, y=60)
        if 'ALMA1008' in permisos:
            self.buttonEditCategory = customtkinter.CTkButton(self.frame_category,  text="Editar\nCategoria", width=80, height=60, state='normal', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
            self.buttonEditCategory.place(x=375, y=60)
        else: 
            self.buttonEditCategory = customtkinter.CTkButton(self.frame_category,  text="Editar\nCategoria", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
            self.buttonEditCategory.place(x=375, y=60)
        if 'ALMA1010' in permisos:
            self.buttonDisableCategory = customtkinter.CTkButton(self.frame_category,  text="Desactivar\nCategoria", width=80, height=60, state='enabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableCategory.place(x=490, y=60)
        else:
            self.buttonDisableCategory = customtkinter.CTkButton(self.frame_category,  text="Desactivar\nCategoria", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableCategory.place(x=490, y=60)
        # Borrar los elementos existentes en la tabla de permisos
        self.categoryTable.delete(*self.categoryTable.get_children())
        self.categoryTable.heading('#4', text='Updated_at')
        # Obtener la lista de permisos activos
        active_category = listCategory()
        # Insertar los permisos activos en la tabla
        for i, p in enumerate(active_category):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.categoryTable.insert('',0,text=p[0], values=(p[1],p[2],p[3]), tags=(tag,))


    def showInactive(self, permisos):
        self.buttonCreateCategory = customtkinter.CTkButton(self.frame_category, text="Nuevo\nCategoria", width=80, height=60, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.FormNewDepot(permisos))
        self.buttonCreateCategory.place(x=260, y=60)
        if 'ALMA1004' in permisos:
            self.buttonEditCategory = customtkinter.CTkButton(self.frame_category,  text="Editar\nCategoria", width=80, height=60, state='normal', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
            self.buttonEditCategory.place(x=375, y=60)
        else: 
            self.buttonEditCategory = customtkinter.CTkButton(self.frame_category,  text="Editar\nCategoria", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
            self.buttonEditCategory.place(x=375, y=60)
        if 'ALMA1013' in permisos:
            self.buttonDisableCategory = customtkinter.CTkButton(self.frame_category,  text="Desactivar\nCategoria", width=80, height=60, state='enabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableCategory.place(x=490, y=60)
        else:
            self.buttonDisableCategory = customtkinter.CTkButton(self.frame_category,  text="Desactivar\nCategoria", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableCategory.place(x=490, y=60)

        self.categoryTable.delete(*self.categoryTable.get_children())
        inactive_category = inactive_cat()
        for i, p in enumerate(inactive_category):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.categoryTable.insert('',0,text=p[0], values=(p[1],p[2],p[3]), tags=(tag,))

    def updateSearch(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_categoria.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM category WHERE
                        id LIKE ? OR 
                        name_category LIKE ? OR 
                        created_at LIKE ? OR
                        updated_at LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.Listacategoria:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.categoryTable.delete(*self.categoryTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.categoryTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
        self.cursor.close()
        self.connection.close()

    def FormCreateCategory(self, permisos):
       self.id = None
       #Creacion del top level
       self.topCreateCat = customtkinter.CTkToplevel()
       self.topCreateCat.title("Crear category")
       self.topCreateCat.w = 500
       self.topCreateCat.h = 300
       self.topCreateCat.geometry(f"{self.topCreateCat.w}x{self.topCreateCat.h}")
       self.topCreateCat.resizable(False, False)
       self.topCreateCat.configure(bg_color='#6a717e')
       self.topCreateCat.configure(fg_color='#6a717e')
       centerWindow(self.topCreateCat)
       set_window_icon(self.topCreateCat)
       self.topCreateCat.lift()
       self.topCreateCat.grab_set()
       self.topCreateCat.transient()
   
       frame_createCat = customtkinter.CTkFrame(self.topCreateCat, width=450,height=250, bg_color="white", fg_color="white")
       frame_createCat.place(relx=0.50, rely=0.5, anchor="center")
       
       set_opacity(frame_createCat, 0.8)
   
       self.lblinfo = customtkinter.CTkLabel(frame_createCat, text="Crear una Categoria", font=("Roboto",13))
       self.lblinfo.place(x=170, rely=0.1)
   
       self.lblnombre_category = customtkinter.CTkLabel(frame_createCat, text='Nombre de la categoria', font=("Roboto", 13))
       self.lblnombre_category.place(x=162, y=70)
   
       self.svnombre_category = customtkinter.StringVar()
       self.entrynombre_category = ttk.Entry(frame_createCat, style='Modern.TEntry', textvariable=self.svnombre_category)
       self.entrynombre_category.place(x=164, y=100)
       self.entrynombre_category.configure(style='Entry.TEntry')
   
       self.buttonCrearcategory = tk.Button(frame_createCat, text="Crear \nCategoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.SaveCategory)
       self.buttonCrearcategory.place(x=182, y=160)

    def FormEditCategory(self, permisos, values):
        if values:
            self.id = self.categoryTable.item(self.categoryTable.selection())['text']
            self.svedit_nombrecategory = self.categoryTable.item(self.categoryTable.selection())['values'][1]

            #Creacion del top level
            self.topEditCat = customtkinter.CTkToplevel()
            self.topEditCat.title("Editar category")
            self.topEditCat.w = 550
            self.topEditCat.h = 300
            self.topEditCat.geometry(f"{self.topEditCat.w}x{self.topEditCat.h}")
            self.topEditCat.resizable(False, False)
            self.topEditCat.configure(bg_color='#6a717e')
            self.topEditCat.configure(fg_color='#6a717e')
            set_window_icon(self.topEditCat)
            centerWindow(self.topEditCat)
            self.topEditCat.lift()
            self.topEditCat.grab_set()
            self.topEditCat.transient()

            frame_editCat = customtkinter.CTkFrame(self.topEditCat, width=450,height=250, bg_color="white", fg_color="white")
            frame_editCat.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(frame_editCat, 0.8)

            self.lblinfo = customtkinter.CTkLabel(frame_editCat, text="Editar una Categoria", font=("Roboto",13))
            self.lblinfo.place(x=170, rely=0.1)

            self.lblnombre_category = customtkinter.CTkLabel(frame_editCat, text='Nombre de la categoria', font=("Roboto", 13))
            self.lblnombre_category.place(x=162, y=70)

            self.svnombre_category = customtkinter.StringVar(value=self.svedit_nombrecategory)
            self.entrynombre_category = ttk.Entry(frame_editCat, style='Modern.TEntry', textvariable=self.svnombre_category)
            self.entrynombre_category.place(x=164, y=100)
            self.entrynombre_category.configure(style='Entry.TEntry')

            self.buttonActualizarcategory = tk.Button(frame_editCat, text="Actualizar \nCategoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.SaveCategory)
            self.buttonActualizarcategory.place(x=178, y=160)
        else:
            messagebox.showerror("Error", "Debe seleccionar una categoria")
    def SaveCategory(self):
        id_cat = buscarCorrelativo('categoria')
        id_cat = id_cat + 1
    
        fecha_actual = datetime.datetime.now()
        created_at = fecha_actual.strftime("%Y-%M-%d")
        updated_at = fecha_actual.strftime("%Y-%M-%d %H:%M:%S")
        Category = category(
            self.svnombre_category.get(),
            created_at,
            updated_at,
            deleted_at = 'NULL'
        )
    
        if self.id is None:
            save_cat(Category)
            actualizarCorrelativo('categoria')
            self.topCreateCat.destroy()
        else:
            edit_cat(Category, self.id)
            self.topEditCat.destroy()
        self.updateTable()
    def categoryDisable(self, permisos):
        try:
            self.id = self.categoryTable.item(self.categoryTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas desactivar este categoria?")

            if confirmar:
                catDisable(self.id)
                self.updateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarDeposito, form_category: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    def restoreCategory(self, permisos):
        try:
            self.id = self.categoryTable.item(self.categoryTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas restaurar esta category?")

            if confirmar:
                recoverCategory(self.id)
                self.switchStatus.select(True)
                self.showStatus(permisos)
                self.updateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en restoreCategory, form_category: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    def updateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.categoryTable.delete(*self.categoryTable.get_children())

            if where is not None and len(where) > 0:
                self.catList = searchCategories(where)
            else:
                self.catList = listCategory()
                self.catList.reverse()

            for p in self.catList:
                self.categoryTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en updateTable, form_category: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')