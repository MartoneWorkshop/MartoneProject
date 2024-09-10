import tkinter as tk
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.CategoryDao import category, save_cat, edit_cat, searchCategories, listCategory, catDisable, inactive_cat
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

        self.marco_categoria = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_categoria.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_categoria, 0.8)
        
        self.buttonCreateGroup = tk.Button(self.marco_categoria, text="Crear\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.FormCreateCategory(permisos))
        self.buttonCreateGroup.place(x=260, y=60)

        self.buttonedit_cat = tk.Button(self.marco_categoria, text="Editar\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.FormEditCategory(permisos, self.categoryTable.item(self.categoryTable.selection())['values']))
        self.buttonedit_cat.place(x=375, y=60)

        self.buttonDisableGroup = tk.Button(self.marco_categoria, text="Desactivar\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.categoryDisable(permisos))
        self.buttonDisableGroup.place(x=490, y=60)
        
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_categoria = customtkinter.CTkLabel(self.marco_categoria, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_categoria.place(x=240, y=155)

        self.sventrysearch_categoria = customtkinter.StringVar()
        self.entrysearch_categoria = ttk.Entry(self.marco_categoria, textvariable=self.sventrysearch_categoria, style='Modern.TEntry', width=30)
        self.entrysearch_categoria.place(x=290, y=157)
        self.entrysearch_categoria.bind('<KeyRelease>', self.updateSearch)

        self.switchStatus = tk.BooleanVar(value=True)
        self.switchCatStatus = customtkinter.CTkSwitch(self.marco_categoria, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.showStatus)
        self.switchCatStatus.place(x=720, y=157)

        #################################################### INFORMACION DE LA TABLA ####################################################
        
        where = ""
        if len(where) > 0:
            self.Listacategoria = searchCategories(where)
        else:
            self.Listacategoria = listCategory()
            self.Listacategoria.reverse()

        self.categoryTable = ttk.Treeview(self.marco_categoria, column=('name_group','created_at','updated_at'), height=25)
        self.categoryTable.place(x=235, y=200)

        self.scroll = ttk.Scrollbar(self.marco_categoria, orient='vertical', command=self.categoryTable.yview)
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


        for p in self.Listacategoria:
            self.categoryTable.insert('',0,text=p[0], values=(p[1],p[2],p[3]))

        self.categoryTable.bind('<Double-1>', lambda event: self.FormEditCategory(event, self.categoryTable.item(self.categoryTable.selection())['values']))

    def showStatus(self):
        if self.switchStatus.get():
            self.switchCatStatus.configure(text="Activos")
            self.showActive()
        else:
            self.switchCatStatus.configure(text="Inactivos")
            self.showInactive()   
    def showActive(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.categoryTable.delete(*self.categoryTable.get_children())
        # Obtener la lista de permisos activos
        acitveCats = listCategory()
        # Insertar los permisos activos en la tabla
        for p in acitveCats:
            self.categoryTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))
    def showInactive(self):
        self.categoryTable.delete(*self.categoryTable.get_children())
        categoria_desactivados = inactive_cat()
        for p in categoria_desactivados:
            self.categoryTable.insert('',0, text=p[0], values=(p[1],p[2],p[3]))
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
       
       #Centrar la ventana en la pantalla
       screen_width = self.topCreateCat.winfo_screenwidth()
       screen_height = self.topCreateCat.winfo_screenheight()
       x = (screen_width - self.topCreateCat.w) // 2
       y = (screen_height - self.topCreateCat.h) // 2
       self.topCreateCat.geometry(f"+{x}+{y}")
   
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

            #Centrar la ventana en la pantalla
            screen_width = self.topEditCat.winfo_screenwidth()
            screen_height = self.topEditCat.winfo_screenheight()
            x = (screen_width - self.topEditCat.w) // 2
            y = (screen_height - self.topEditCat.h) // 2
            self.topEditCat.geometry(f"+{x}+{y}")

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