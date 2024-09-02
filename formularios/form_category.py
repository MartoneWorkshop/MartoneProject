import tkinter as tk
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.GruposDao import Grupo, SaveGroup, EditGroup, InformacionGrupos, ListarGrupos, consulCat, GroupDisable, GruposDesactivados
from config import COLOR_MENU_LATERAL
import datetime
from tkinter import messagebox
import sqlite3


class FormCategoria():

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

        self.marco_categoria = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_categoria.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_categoria, 0.8)
        
        self.buttonCreateGroup = tk.Button(self.marco_categoria, text="Crear\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.crear_grupo(permisos))
        self.buttonCreateGroup.place(x=260, y=60)

        self.buttonEditGroup = tk.Button(self.marco_categoria, text="Editar\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.editar_grupo(permisos, self.tablacategoria.item(self.tablacategoria.selection())['values']))
        self.buttonEditGroup.place(x=375, y=60)

        self.buttonDisableGroup = tk.Button(self.marco_categoria, text="Desactivar\n Categoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarGrupo(permisos))
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
        self.entrysearch_categoria.bind('<KeyRelease>', self.update_cat_content)

        self.switchStatus = tk.BooleanVar(value=True)
        self.switchCatStatus = customtkinter.CTkSwitch(self.marco_categoria, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
        self.switchCatStatus.place(x=720, y=157)

        #################################################### INFORMACION DE LA TABLA ####################################################
        
        where = ""
        if len(where) > 0:
            self.Listacategoria = consulCat(where)
        else:
            self.Listacategoria = ListarGrupos()
            self.Listacategoria.reverse()

        self.tablacategoria = ttk.Treeview(self.marco_categoria, column=('codgrupo','name_group','date_created','date_update'), height=25)
        self.tablacategoria.place(x=235, y=200)

        self.scroll = ttk.Scrollbar(self.marco_categoria, orient='vertical', command=self.tablacategoria.yview)
        self.scroll.place(x=788, y=200, height=526)

        self.tablacategoria.configure(yscrollcommand=self.scroll.set)
        self.tablacategoria.tag_configure('evenrow')

        self.tablacategoria.heading('#0',text="ID")
        self.tablacategoria.heading('#1',text="CodGrupo")
        self.tablacategoria.heading('#2',text="Nombre Grupo")
        self.tablacategoria.heading('#3',text="Date-Created")
        self.tablacategoria.heading('#4',text="Date-Update")

        self.tablacategoria.column("#0", width=50, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablacategoria.column("#1", width=100, stretch=False)
        self.tablacategoria.column("#2", width=150, stretch=False)
        self.tablacategoria.column("#3", width=125, stretch=False)
        self.tablacategoria.column("#4", width=125, stretch=False)

        for p in self.Listacategoria:
            self.tablacategoria.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4]))

        self.tablacategoria.bind('<Double-1>', lambda event: self.editar_grupo(event, self.tablacategoria.item(self.tablacategoria.selection())['values']))

    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchCatStatus.configure(text="Activos")
            self.mostrarCatActivos()
        else:
            self.switchCatStatus.configure(text="Inactivos")
            self.mostrarCatDesactivados()
     
    def mostrarCatActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablacategoria.delete(*self.tablacategoria.get_children())
        # Obtener la lista de permisos activos
        categoria_activos = ListarGrupos()
        # Insertar los permisos activos en la tabla
        for p in categoria_activos:
            self.tablacategoria.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))

    def mostrarCatDesactivados(self):
        self.tablacategoria.delete(*self.tablacategoria.get_children())
        categoria_desactivados = GruposDesactivados()
        for p in categoria_desactivados:
            self.tablacategoria.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4]))

    def update_cat_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_categoria.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM grupo WHERE
                        id LIKE ? OR 
                        codgrupo LIKE ? OR 
                        name_group LIKE ? OR 
                        date_created LIKE ? OR
                        date_update LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.listaGrupo:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablacategoria.delete(*self.tablacategoria.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablacategoria.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()

    def crear_grupo(self, permisos):
       self.id = None
       #Creacion del top level
       self.topCreateGroup = customtkinter.CTkToplevel()
       self.topCreateGroup.title("Crear Grupo")
       self.topCreateGroup.w = 500
       self.topCreateGroup.h = 300
       self.topCreateGroup.geometry(f"{self.topCreateGroup.w}x{self.topCreateGroup.h}")
       self.topCreateGroup.resizable(False, False)
       self.topCreateGroup.configure(bg_color='#6a717e')
       self.topCreateGroup.configure(fg_color='#6a717e')
       
       #Centrar la ventana en la pantalla
       screen_width = self.topCreateGroup.winfo_screenwidth()
       screen_height = self.topCreateGroup.winfo_screenheight()
       x = (screen_width - self.topCreateGroup.w) // 2
       y = (screen_height - self.topCreateGroup.h) // 2
       self.topCreateGroup.geometry(f"+{x}+{y}")
   
       self.topCreateGroup.lift()
       self.topCreateGroup.grab_set()
       self.topCreateGroup.transient()
   
       marco_createGroup = customtkinter.CTkFrame(self.topCreateGroup, width=450,height=250, bg_color="white", fg_color="white")
       marco_createGroup.place(relx=0.50, rely=0.5, anchor="center")
       
       set_opacity(marco_createGroup, 0.8)
   
       self.lblinfo = customtkinter.CTkLabel(marco_createGroup, text="Crear una Categoria", font=("Roboto",13))
       self.lblinfo.place(x=170, rely=0.1)
   
       self.lblnombre_grupo = customtkinter.CTkLabel(marco_createGroup, text='Nombre de la categoria', font=("Roboto", 13))
       self.lblnombre_grupo.place(x=162, y=70)
   
       self.svnombre_grupo = customtkinter.StringVar()
       self.entrynombre_grupo = ttk.Entry(marco_createGroup, style='Modern.TEntry', textvariable=self.svnombre_grupo)
       self.entrynombre_grupo.place(x=164, y=100)
       self.entrynombre_grupo.configure(style='Entry.TEntry')
   
       self.buttonCrearGrupo = tk.Button(marco_createGroup, text="Crear \nCategoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarGrupo)
       self.buttonCrearGrupo.place(x=182, y=160)
   
    def editar_grupo(self, permisos, values):
        if values:
            self.id = self.tablacategoria.item(self.tablacategoria.selection())['text']
            self.editarnombre_grupo = self.tablacategoria.item(self.tablacategoria.selection())['values'][0]

            #Creacion del top level
            self.topEditGroup = customtkinter.CTkToplevel()
            self.topEditGroup.title("Editar Grupo")
            self.topEditGroup.w = 550
            self.topEditGroup.h = 300
            self.topEditGroup.geometry(f"{self.topEditGroup.w}x{self.topEditGroup.h}")
            self.topEditGroup.resizable(False, False)
            self.topEditGroup.configure(bg_color='#6a717e')
            self.topEditGroup.configure(fg_color='#6a717e')

            #Centrar la ventana en la pantalla
            screen_width = self.topEditGroup.winfo_screenwidth()
            screen_height = self.topEditGroup.winfo_screenheight()
            x = (screen_width - self.topEditGroup.w) // 2
            y = (screen_height - self.topEditGroup.h) // 2
            self.topEditGroup.geometry(f"+{x}+{y}")

            self.topEditGroup.lift()
            self.topEditGroup.grab_set()
            self.topEditGroup.transient()

            marco_EditGroup = customtkinter.CTkFrame(self.topEditGroup, width=450,height=250, bg_color="white", fg_color="white")
            marco_EditGroup.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(marco_EditGroup, 0.8)

            self.lblinfo = customtkinter.CTkLabel(marco_EditGroup, text="Editar una Categoria", font=("Roboto",13))
            self.lblinfo.place(x=170, rely=0.1)

            self.lblnombre_grupo = customtkinter.CTkLabel(marco_EditGroup, text='Nombre de la categoria', font=("Roboto", 13))
            self.lblnombre_grupo.place(x=162, y=70)

            self.svnombre_grupo = customtkinter.StringVar()
            self.entrynombre_grupo = ttk.Entry(marco_EditGroup, style='Modern.TEntry', textvariable=self.svnombre_grupo)
            self.entrynombre_grupo.place(x=164, y=100)
            self.entrynombre_grupo.configure(style='Entry.TEntry')

            self.buttonActualizarGrupo = tk.Button(marco_EditGroup, text="Actualizar \nCategoria", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarGrupo)
            self.buttonActualizarGrupo.place(x=178, y=160)
        else:
            messagebox.showerror("Error", "Debe seleccionar una categoria")

    def GuardarGrupo(self):
        codGrupo = buscarCorrelativo('grupo')
        codGrupo = codGrupo + 1
    
        fecha_actual = datetime.datetime.now()
        date_created = fecha_actual.strftime("%d/%m/%Y")
        date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
        grupo = Grupo(
            codGrupo,
            self.svnombre_grupo.get(),
            date_created,
            date_update
        )
    
        if self.id is None:
            SaveGroup(grupo)
            actualizarCorrelativo('grupo')
            self.topCreateGroup.destroy()
        else:
            EditGroup(grupo, self.id)
            self.topEditGroup.destroy()
        self.listarGrupoEnTabla()

    def desactivarGrupo(self, permisos):
        try:
            self.id = self.tablacategoria.item(self.tablacategoria.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas desactivar este grupo?")

            if confirmar:
                GroupDisable(self.id)
                self.listarGrupoEnTabla()

        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarDeposito, form_category: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarGrupoEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablacategoria.delete(*self.tablacategoria.get_children())

            if where is not None and len(where) > 0:
                self.listaGrupo = InformacionGrupos(where)
            else:
                self.listaGrupo = ListarGrupos()
                self.listaGrupo.reverse()

            for p in self.listaGrupo:
                self.tablacategoria.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarGrupoEnTabla, form_category: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')