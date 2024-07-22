import tkinter as tk
from tkinter import ttk, OptionMenu, Tk, Menu
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import customtkinter
import PIL
from PIL import Image, ImageTk
from tkinter import messagebox
from util.util_alerts import edit_advice, error_advice, save_advice, set_opacity
from functions.conexion import ConexionDB
from util.util_functions import obtener_permisos, ObtenerListaDeModulos, ObtenerPermisosDeModulos, ObtenerRoles, buscarCorrelativo, actualizarCorrelativo, ObtenerModulos
from functions.ProvDao import Proveedores, consulProv, listarProveedores, SaveProv, EditProv, ProvDisable, ProveedoresDesactivados
import sqlite3
import datetime
import ctypes

class FormProv():
    def __init__(self, cuerpo_principal, permisos):
        self.id = None
        # Crear paneles: barra superior 
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 
        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  
        # Segundo Label con la imagen
        ruta_imagen = "imagenes/background.png"
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_tk = imagen_tk
        # Crear el Label con la imagen de fondo
        label_fondo = tk.Label(cuerpo_principal, image=imagen_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_fondo = label_fondo
        
        def ajustar_imagen(event):
            # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
            nueva_imagen = imagen.resize((event.width, event.height))
            nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.imagen_tk = nueva_imagen_tk
            # Actualizar la imagen en el Label de fondo
            label_fondo.config(image=nueva_imagen_tk)
            
        self.barra_inferior.bind("<Configure>", ajustar_imagen)
        
        bg = imagen_tk

        self.marco_prov = customtkinter.CTkFrame(cuerpo_principal, width=1150, height=800, bg_color="white", fg_color="white")
        self.marco_prov.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_prov, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateProv = tk.Button(self.marco_prov, text="Crear\n Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_proveedor(permisos, bg))
        self.buttonCreateProv.place(x=140, y=50)

        self.buttonEditProv = tk.Button(self.marco_prov, text="Editar\n Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_proveedor(permisos, self.tablaProveedores.item(self.tablaProveedores.selection())['values']))
        self.buttonEditProv.place(x=265, y=50)

        if 'CONF1009' in permisos:
            self.buttonDeleteProv = tk.Button(self.marco_prov, text="Desactivar\n Proveedor", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarProveedor(permisos))
            self.buttonDeleteProv.place(x=390, y=50)
        else:
            self.buttonDeleteProv = tk.Button(self.marco_prov, text="Desactivar\n Proveedor", font=("Roboto", 12), state='disabled', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.desactivarProveedor(permisos))
            self.buttonDeleteProv.place(x=390, y=50)

        if 'CONF1015' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchProvStatus = customtkinter.CTkSwitch(self.marco_prov, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchProvStatus.place(x=900, y=157)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchProvStatus = customtkinter.CTkSwitch(self.marco_prov, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
            self.switchProvStatus.place(x=900, y=157)
    
        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_proveedors = customtkinter.CTkLabel(self.marco_prov, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_proveedors.place(x=65, y=155)

        self.sventrysearch_proveedores = customtkinter.StringVar()
        self.entrysearch_proveedores = ttk.Entry(self.marco_prov, textvariable=self.sventrysearch_proveedores, style='Modern.TEntry', width=30)
        self.entrysearch_proveedores.place(x=100, y=157)
        self.entrysearch_proveedores.bind('<KeyRelease>', self.update_prov_content)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.ListaProveedores = consulProv(where)
        else:
            self.ListaProveedores = listarProveedores()
            self.ListaProveedores.reverse()

        self.tablaProveedores = ttk.Treeview(self.marco_prov, column=('codprov','nom_fiscal','rif_prov','nit_prov','tipo_per','email_prov','telf_prov','dir_fiscal','dias_credito'), height=25)
        self.tablaProveedores.place(x=22, y=200)

        self.scroll = ttk.Scrollbar(self.marco_prov, orient='vertical', command=self.tablaProveedores.yview)
        self.scroll.place(x=1104, y=200, height=526)

        self.tablaProveedores.configure(yscrollcommand=self.scroll.set)
        self.tablaProveedores.tag_configure('evenrow')

        self.tablaProveedores.heading('#0',text="ID")
        self.tablaProveedores.heading('#1',text="CodProv")
        self.tablaProveedores.heading('#2',text="N Fiscal")
        self.tablaProveedores.heading('#3',text="RIF")
        self.tablaProveedores.heading('#4',text="NIT")
        self.tablaProveedores.heading('#5',text="Tipo P")
        self.tablaProveedores.heading('#6',text="Email")
        self.tablaProveedores.heading('#7',text="Telefono")
        self.tablaProveedores.heading('#8',text="Dir-Fiscal")
        self.tablaProveedores.heading('#9',text="Dias Credito")

        self.tablaProveedores.column("#0", width=50, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaProveedores.column("#1", width=50, stretch=False)
        self.tablaProveedores.column("#2", width=150, stretch=False)
        self.tablaProveedores.column("#3", width=100, stretch=False)
        self.tablaProveedores.column("#4", width=100, stretch=False)
        self.tablaProveedores.column("#5", width=100, stretch=False)
        self.tablaProveedores.column("#6", width=150, stretch=False)
        self.tablaProveedores.column("#7", width=100, stretch=False)
        self.tablaProveedores.column("#8", width=200, stretch=False)
        self.tablaProveedores.column("#9", width=80, stretch=False)

        for p in self.ListaProveedores:
            self.tablaProveedores.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9]))

        self.tablaProveedores.bind('<Double-1>', lambda event: self.editar_proveedor(event, self.tablaProveedores.item(self.tablaProveedores.selection())['values']))
    
    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchProvStatus.configure(text="Activos")
            self.mostrarProveedoresActivos()
        else:
            self.switchProvStatus.configure(text="Inactivos")
            self.mostrarProveedoresDesactivados()

    def mostrarProveedoresActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaProveedores.delete(*self.tablaProveedores.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listarProveedores()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaProveedores.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6]))

    def mostrarProveedoresDesactivados(self):
        self.tablaProveedores.delete(*self.tablaProveedores.get_children())
        permisos_desactivados = ProveedoresDesactivados()
        for p in permisos_desactivados:
            self.tablaProveedores.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))

    def update_prov_content(self, event=None):
        conexion = ConexionDB()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_proveedores.get()
    # Realizar la consulta
        sql = """SELECT * FROM proveedores WHERE
                id LIKE ? OR 
                codprov LIKE ? OR 
                nom_fiscal LIKE ? OR 
                rif_prov LIKE ? OR 
                nit_prov LIKE ? OR
                tipo_per LIKE ? OR 
                email_prov LIKE ? OR 
                telf_prov LIKE ? OR 
                dir_fiscal LIKE ? OR
                dias_credito LIKE ?"""
        parametros = ('%' + self.content + '%',
                '%' + self.content + '%',  
                '%' + self.content + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%',
                '%' + self.content.strip() + '%', 
                '%' + self.content.strip() + '%')
        conexion.ejecutar_consulta_parametros(sql, parametros)
        resultados = conexion.obtener_resultados()  
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.ListaProveedores:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower() or self.content.lower() in str(p[7]).lower() or self.content.lower() in str(p[8]).lower() or self.content.lower() in str(p[9]).lower()  or self.content.lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaProveedores.delete(*self.tablaProveedores.get_children())
    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaProveedores.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]))
        conexion.cerrarConexion()

    def crear_proveedor(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateProv = customtkinter.CTkToplevel()
        self.topCreateProv.title("Crear Proveedor")
        self.topCreateProv.w = 800
        self.topCreateProv.h = 600
        self.topCreateProv.geometry(f"{self.topCreateProv.w}x{self.topCreateProv.h}")
        self.topCreateProv.resizable(False, False)
        self.topCreateProv.configure(bg_color='#6a717e')
        self.topCreateProv.configure(fg_color='#6a717e')

        #Centrar la ventana en la pantalla
        screen_width = self.topCreateProv.winfo_screenwidth()
        screen_height = self.topCreateProv.winfo_screenheight()
        x = (screen_width - self.topCreateProv.w) // 2
        y = (screen_height - self.topCreateProv.h) // 2
        self.topCreateProv.geometry(f"+{x}+{y}")

        self.topCreateProv.lift()
        self.topCreateProv.grab_set()
        self.topCreateProv.transient()
        selected_item = self.tablaProveedores.focus()
        values = self.tablaProveedores.item(selected_item)['values']
        #Datos para el proveedor
        marco_crearproveedor = customtkinter.CTkFrame(self.topCreateProv, width=750,height=550, bg_color="white", fg_color="white")
        marco_crearproveedor.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_crearproveedor, 0.8)
        self.lblinfo = customtkinter.CTkLabel(marco_crearproveedor, text="Creacion de nuevo proveedor", font=("Roboto",14))
        self.lblinfo.place(relx=0.4, rely=0.05)

        #RIF
        self.lblrif_prov = customtkinter.CTkLabel(marco_crearproveedor, text='RIF', font=("Roboto", 13))
        self.lblrif_prov.place(x=75, y=90)
        
        self.svrif_prov = customtkinter.StringVar()
        self.entryrif_prov = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svrif_prov)
        self.entryrif_prov.place(x=65, y=120)
        self.entryrif_prov.configure(style='Entry.TEntry')
        self.entryrif_prov.insert(0, self.svrif_prov.get())

        #Nombre Fiscal
        self.lblnom_fiscal = customtkinter.CTkLabel(marco_crearproveedor, text='Nombre Fiscal', font=("Roboto", 13))
        self.lblnom_fiscal.place(x=275, y=90)

        self.svnom_fiscal = customtkinter.StringVar()
        self.entrynom_fiscal = ttk.Entry(marco_crearproveedor, width=35, style='Modern.TEntry', textvariable=self.svnom_fiscal)
        self.entrynom_fiscal.place(x=265, y=120)
        self.entrynom_fiscal.configure(style='Entry.TEntry')


        #Tipo Persona Esto es un multi options editar despues
        self.lbltipo_per = customtkinter.CTkLabel(marco_crearproveedor, text='Tipo de Persona', font=("Roboto", 13))
        self.lbltipo_per.place(x=550, y=90)
        
        self.svtipo_per = customtkinter.StringVar(value="Seleccione el Tipo")

        self.multioption = customtkinter.CTkOptionMenu(marco_crearproveedor, values=["V (NATURAL)", "J (JURIDICO)", "E (EXTRANJERO)", "G (GUBERNAMENTAL)"], width=140, variable=self.svtipo_per)
        self.multioption.place(x=530, y=115)

        def update_rif_prefix(*args):
            selected_option = self.svtipo_per.get()
            rif_value = self.svrif_prov.get()
            prefix = ""

            if selected_option == "V (NATURAL)":
                prefix = "V-"
            elif selected_option == "E (EXTRANJERO)":
                prefix = "E-"
            elif selected_option == "J (JURIDICO)":
                prefix = "J-"
            elif selected_option == "G (GUBERNAMENTAL)":
                prefix = "G-"

            if rif_value.startswith("V-"):
                rif_value = rif_value[2:]

            elif rif_value.startswith("E-"):
                rif_value = rif_value[2:]

            elif rif_value.startswith("J-"):
                rif_value = rif_value[2:]

            elif rif_value.startswith("G-"):
                rif_value = rif_value[2:]

            self.svrif_prov.set(f"{prefix}{rif_value}")
        self.svtipo_per.trace("w", update_rif_prefix)

        #NIT
        self.lblnit_prov = customtkinter.CTkLabel(marco_crearproveedor, text='NIT', font=("Roboto", 13))
        self.lblnit_prov.place(x=75, y=180)

        self.svnit_prov = customtkinter.StringVar()
        self.entrynit_prov = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svnit_prov)
        self.entrynit_prov.place(x=65, y=210)
        self.entrynit_prov.configure(style='Entry.TEntry')
        
        #Email
        self.lblemail_prov = customtkinter.CTkLabel(marco_crearproveedor, text='Email', font=("Roboto", 13))
        self.lblemail_prov.place(x=275, y=180)

        self.svemail_prov = customtkinter.StringVar()
        self.entryemail_prov = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svemail_prov, width=35)
        self.entryemail_prov.place(x=265, y=210)
        self.entryemail_prov.configure(style='Entry.TEntry')

        #Telefono
        self.lbltelf_prov = customtkinter.CTkLabel(marco_crearproveedor, text='Telefono', font=("Roboto", 13))
        self.lbltelf_prov.place(x=550, y=180)

        self.svtelf_prov = customtkinter.StringVar()
        self.entrytelf_prov = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svtelf_prov)
        self.entrytelf_prov.place(x=540, y=210)
        self.entrytelf_prov.configure(style='Entry.TEntry')        

        ##Textbox para dir_fiscal
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
                self.dir_fiscal.delete("1.141", "end")

                self.dir_fiscal.configure(state="normal")
                self.dir_fiscal.delete("1.0", "end")
                self.dir_fiscal.insert("1.0", text)
        
        self.lbldir_fiscal = customtkinter.CTkLabel(marco_crearproveedor, text='Direccion Fiscal', font=("Roboto", 13))
        self.lbldir_fiscal.place(x=75, y=270)

        self.dir_fiscal = customtkinter.CTkTextbox(marco_crearproveedor, width=410, height=55, border_width=1)
        self.dir_fiscal.place(x=65, y=300)

        character_count_label = customtkinter.CTkLabel(marco_crearproveedor, text="")
        character_count_label.place(x=440, y=360)

        def on_text_change(event):
            validate_text(self.dir_fiscal.get("1.0", "end-1c"))

        self.dir_fiscal.bind("<KeyRelease>", on_text_change)
        
        #Dias de Credito
        self.lbldias_credito = customtkinter.CTkLabel(marco_crearproveedor, text='Dias de Credito', font=("Roboto", 13))
        self.lbldias_credito.place(x=550, y=270)

        self.svdias_credito = customtkinter.StringVar()
        self.entrydias_credito = ttk.Entry(marco_crearproveedor, style='Modern.TEntry', textvariable=self.svdias_credito)
        self.entrydias_credito.place(x=540, y=300)
        self.entrydias_credito.configure(style='Entry.TEntry')

        self.buttonGuardarProv = tk.Button(marco_crearproveedor, text="Guardar Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                            compound=tk.LEFT, padx=10, command=self.GuardarProveedor)
        self.buttonGuardarProv.place(relx=0.4, y=500)

    def editar_proveedor(self, permisos, values):   
        if values:
    # Creación del top level
            self.id = self.tablaProveedores.item(self.tablaProveedores.selection())['text']
            self.nom_fiscal = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][1]
            self.rif_prov = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][2]
            self.nit_prov = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][3]
            self.tipo_per = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][4]
            self.email_prov = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][5]
            self.telf_prov = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][6]
            self.Edir_fiscal = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][7]
            self.dias_credito = self.tablaProveedores.item(self.tablaProveedores.selection())['values'][8]

            self.topEditProv = customtkinter.CTkToplevel()
            self.topEditProv.title("Crear Proveedor")
            self.topEditProv.w = 800
            self.topEditProv.h = 600
            self.topEditProv.geometry(f"{self.topEditProv.w}x{self.topEditProv.h}")
            self.topEditProv.resizable(False, False)
            self.topEditProv.configure(bg_color='#6a717e')
            self.topEditProv.configure(fg_color='#6a717e')

            #Centrar la ventana en la pantalla
            screen_width = self.topEditProv.winfo_screenwidth()
            screen_height = self.topEditProv.winfo_screenheight()
            x = (screen_width - self.topEditProv.w) // 2
            y = (screen_height - self.topEditProv.h) // 2
            self.topEditProv.geometry(f"+{x}+{y}")

            self.topEditProv.lift()
            self.topEditProv.grab_set()
            self.topEditProv.transient()
            selected_item = self.tablaProveedores.focus()
            values = self.tablaProveedores.item(selected_item)['values']
            #Datos para el proveedor
            marco_editarproveedor = customtkinter.CTkFrame(self.topEditProv, width=750,height=550, bg_color="white", fg_color="white")
            marco_editarproveedor.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(marco_editarproveedor, 0.8)
            self.lblinfo = customtkinter.CTkLabel(marco_editarproveedor, text="Editar un proveedor", font=("Roboto",14))
            self.lblinfo.place(relx=0.4, rely=0.05)

            #RIF
            self.lblrif_prov = customtkinter.CTkLabel(marco_editarproveedor, text='RIF', font=("Roboto", 13))
            self.lblrif_prov.place(x=75, y=90)

            self.svrif_prov = customtkinter.StringVar(value=self.rif_prov)
            self.entryrif_prov = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svrif_prov)
            self.entryrif_prov.place(x=65, y=120)
            self.entryrif_prov.configure(style='Entry.TEntry')

            #Nombre Fiscal
            self.lblnom_fiscal = customtkinter.CTkLabel(marco_editarproveedor, text='Nombre Fiscal', font=("Roboto", 13))
            self.lblnom_fiscal.place(x=275, y=90)

            self.svnom_fiscal = customtkinter.StringVar(value=self.nom_fiscal)
            self.entrynom_fiscal = ttk.Entry(marco_editarproveedor, width=35, style='Modern.TEntry', textvariable=self.svnom_fiscal)
            self.entrynom_fiscal.place(x=265, y=120)
            self.entrynom_fiscal.configure(style='Entry.TEntry')


            #Tipo Persona Esto es un multi options editar despues
            self.lbltipo_per = customtkinter.CTkLabel(marco_editarproveedor, text='Tipo de Persona', font=("Roboto", 13))
            self.lbltipo_per.place(x=550, y=90)

            self.svtipo_per = customtkinter.StringVar(value=self.tipo_per)

            self.multioption = customtkinter.CTkOptionMenu(marco_editarproveedor, values=["V (NATURAL)", "J (JURIDICO)", "E (EXTRANJERO)", "G (GUBERNAMENTAL)"], width=140, variable=self.svtipo_per)
            self.multioption.place(x=530, y=115)

            def update_rif_prefix(*args):
                selected_option = self.svtipo_per.get()
                rif_value = self.svrif_prov.get()
                prefix = ""

                if selected_option == "V (NATURAL)":
                    prefix = "V-"
                elif selected_option == "E (EXTRANJERO)":
                    prefix = "E-"
                elif selected_option == "J (JURIDICO)":
                    prefix = "J-"
                elif selected_option == "G (GUBERNAMENTAL)":
                    prefix = "G-"

                if rif_value.startswith("V-"):
                    rif_value = rif_value[2:]

                elif rif_value.startswith("E-"):
                    rif_value = rif_value[2:]

                elif rif_value.startswith("J-"):
                    rif_value = rif_value[2:]

                elif rif_value.startswith("G-"):
                    rif_value = rif_value[2:]

                self.svrif_prov.set(f"{prefix}{rif_value}")
            self.svtipo_per.trace("w", update_rif_prefix)

            #NIT
            self.lblnit_prov = customtkinter.CTkLabel(marco_editarproveedor, text='NIT', font=("Roboto", 13))
            self.lblnit_prov.place(x=75, y=180)

            self.svnit_prov = customtkinter.StringVar(value=self.nit_prov)
            self.entrynit_prov = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svnit_prov)
            self.entrynit_prov.place(x=65, y=210)
            self.entrynit_prov.configure(style='Entry.TEntry')

            #Email
            self.lblemail_prov = customtkinter.CTkLabel(marco_editarproveedor, text='Email', font=("Roboto", 13))
            self.lblemail_prov.place(x=275, y=180)

            self.svemail_prov = customtkinter.StringVar(value=self.email_prov)
            self.entryemail_prov = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svemail_prov, width=35)
            self.entryemail_prov.place(x=265, y=210)
            self.entryemail_prov.configure(style='Entry.TEntry')

            #Telefono
            self.lbltelf_prov = customtkinter.CTkLabel(marco_editarproveedor, text='Telefono', font=("Roboto", 13))
            self.lbltelf_prov.place(x=550, y=180)

            self.svtelf_prov = customtkinter.StringVar(value=self.telf_prov)
            self.entrytelf_prov = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svtelf_prov)
            self.entrytelf_prov.place(x=540, y=210)
            self.entrytelf_prov.configure(style='Entry.TEntry')        

            ##Textbox para dir_fiscal
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
                    self.dir_fiscal.delete("1.141", "end")

                    self.dir_fiscal.configure(state="normal")
                    self.dir_fiscal.delete("1.0", "end")
                    self.dir_fiscal.insert("1.0", text)

            self.lbldir_fiscal = customtkinter.CTkLabel(marco_editarproveedor, text='Direccion Fiscal', font=("Roboto", 13))
            self.lbldir_fiscal.place(x=75, y=270)

            self.dir_fiscal = customtkinter.CTkTextbox(marco_editarproveedor, width=410, height=55, border_width=1)
            self.dir_fiscal.place(x=65, y=300)
            self.dir_fiscal.insert("1.0", self.Edir_fiscal)

            character_count_label = customtkinter.CTkLabel(marco_editarproveedor, text="")
            character_count_label.place(x=440, y=360)

            def on_text_change(event):
                validate_text(self.dir_fiscal.get("1.0", "end-1c"))

            self.dir_fiscal.bind("<KeyRelease>", on_text_change)

            #Dias de Credito
            self.lbldias_credito = customtkinter.CTkLabel(marco_editarproveedor, text='Dias de Credito', font=("Roboto", 13))
            self.lbldias_credito.place(x=550, y=270)

            self.svdias_credito = customtkinter.StringVar(value=self.dias_credito)
            self.entrydias_credito = ttk.Entry(marco_editarproveedor, style='Modern.TEntry', textvariable=self.svdias_credito)
            self.entrydias_credito.place(x=540, y=300)
            self.entrydias_credito.configure(style='Entry.TEntry')

            self.buttonGuardarProv = tk.Button(marco_editarproveedor, text="Guardar Proveedor", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0, fg="white", anchor="w", 
                                                compound=tk.LEFT, padx=10, command=self.GuardarProveedor)
            self.buttonGuardarProv.place(relx=0.4, y=500)
        else:
            messagebox.showerror("Error", "Debe seleccionar un proveedor")

    def GuardarProveedor(self):
        try:
            # Otener el contenido del Entry
            codprov = buscarCorrelativo('proveedor')
            actualizarCorrelativo('proveedor')
            codprov = codprov + 1
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")

            proveedor = Proveedores(
                codprov,
                self.svnom_fiscal.get(),
                self.svrif_prov.get(),
                self.svnit_prov.get(),
                self.svtipo_per.get(),
                self.svtelf_prov.get(),
                self.dir_fiscal.get("1.0", "end-1c"),
                self.svemail_prov.get(),
                self.svdias_credito.get(),
                date_created,
                date_update
            )
            
            if self.id is None:
                SaveProv(proveedor)

                self.topCreateProv.destroy()
            else:
                EditProv(proveedor, self.id)
                self.topEditProv.destroy()

            self.listarProveedoresEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarProveedor, form_proveedores: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
    
    def desactivarProveedor(self, permisos):
        try:
            self.id = self.tablaProveedores.item(self.tablaProveedores.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas Seguro de que deseas desactivar este proveedor?")
            if confirmar and 'CONF1011' in permisos:
                ProvDisable(self.id)
                self.listarProveedoresEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarProveedor, form_proveedores: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listarProveedoresEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaProveedores.delete(*self.tablaProveedores.get_children())

            if where is not None and len(where) > 0:
                self.ListaProveedores = consulProv(where)
            else:
                self.ListaProveedores = listarProveedores()
                self.ListaProveedores.reverse()

            for p in self.ListaProveedores:
                self.tablaProveedores.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarProveedoresEnTabla, form_proveedores: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')





    