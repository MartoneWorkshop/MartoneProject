import tkinter as tk
from config import  COLOR_FONDO
import PIL
import sqlite3
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.old_functions import buscarCorrelativo, actualizarCorrelativo
from functions.ClientsDao import Client, save_client, searchClients, clientDelete, clientesDesactivados, listClient, edit_client 
from config import  COLOR_FONDO, WIDTH_LOGO, HEIGHT_LOGO, COLOR_MENU_LATERAL, ANCHO_MENU, ALTO_MENU
import datetime
from tkinter import messagebox


class FormClient():

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

        self.marco_clients = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_clients.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_clients, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateArt = tk.Button(self.marco_clients, text="Crear\n Client", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_cliente(permisos))
        self.buttonCreateArt.place(x=140, y=50)

        self.buttonEditArt = tk.Button(self.marco_clients, text="Editar\n Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.editar_cliente(permisos, self.tablaClients.item(self.tablaClients.selection())['values']))
        self.buttonEditArt.place(x=265, y=50)
            
        self.buttonDeleteArt = tk.Button(self.marco_clients, text="Desactivar\n Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.desactivarClient(permisos))
        self.buttonDeleteArt.place(x=390, y=50)

        #Switch de activos/inactivos
        self.switchStatus = tk.BooleanVar(value=True)
        self.switchArtStatus = customtkinter.CTkSwitch(self.marco_clients, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.MostrarActivosInactivos)
        self.switchArtStatus.place(x=900, y=157)

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_clients = customtkinter.CTkLabel(self.marco_clients, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_clients.place(x=65, y=155)

        self.sventrysearch_clients = customtkinter.StringVar()
        self.entrysearch_clients = ttk.Entry(self.marco_clients, textvariable=self.sventrysearch_clients, style='Modern.TEntry', width=30)
        self.entrysearch_clients.place(x=100, y=157)
        self.entrysearch_clients.bind('<KeyRelease>', self.update_art_content)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.ListaClient = searchClients(where)
        else:            
            self.ListaClient = listClient()
            self.ListaClient.reverse()

        self.tablaClients = ttk.Treeview(self.marco_clients, column=('codClient','codDep','codgrupo','codProv','nombre_cliente','marca','modelo','serial','costo','descripcion'), height=25)
        self.tablaClients.place(x=32, y=200)

        self.scroll = ttk.Scrollbar(self.marco_clients, orient='vertical', command=self.tablaClients.yview)
        self.scroll.place(x=1084, y=200, height=526)

        self.tablaClients.configure(yscrollcommand=self.scroll.set)
        self.tablaClients.tag_configure('evenrow')

        self.tablaClients.heading('#0',text="ID" )
        self.tablaClients.heading('#1',text="CodClient")
        self.tablaClients.heading('#2',text="Deposito")
        self.tablaClients.heading('#3',text="Categoria")
        self.tablaClients.heading('#4',text="Proveedor")
        self.tablaClients.heading('#5',text="Nomb Client")
        self.tablaClients.heading('#6',text="Marca")
        self.tablaClients.heading('#7',text="Modelo")
        self.tablaClients.heading('#8',text="Serial")
        self.tablaClients.heading('#9',text="Costo")
        self.tablaClients.heading('#10',text="Descripcion")

        self.tablaClients.column("#0", width=50, stretch=True, anchor='w')
        self.tablaClients.column("#1", width=100, stretch=True)
        self.tablaClients.column("#2", width=100, stretch=True)
        self.tablaClients.column("#3", width=100, stretch=True)
        self.tablaClients.column("#4", width=100, stretch=True)
        self.tablaClients.column("#5", width=100, stretch=True)
        self.tablaClients.column("#6", width=100, stretch=True)
        self.tablaClients.column("#7", width=100, stretch=True)
        self.tablaClients.column("#8", width=100, stretch=True)
        self.tablaClients.column("#9", width=100, stretch=True)
        self.tablaClients.column("#10", width=100, stretch=True)

        for p in self.ListaClient:
            self.tablaClients.insert('','end',iid=p[0], text=p[0],values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

        self.tablaClients.bind('<Double-1>', lambda event: self.editar_cliente(event, self.tablaClients.item(self.tablaClients.selection())['values']))

    def MostrarActivosInactivos(self):
        if self.switchStatus.get():
            self.switchArtStatus.configure(text="Activos")
            self.mostrarArtActivos()
        else:
            self.switchArtStatus.configure(text="Inactivos")
            self.mostrarArtDesactivados()
     
    def mostrarArtActivos(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.tablaClients.delete(*self.tablaClients.get_children())
        # Obtener la lista de permisos activos
        permisos_activos = listClient()
        # Insertar los permisos activos en la tabla
        for p in permisos_activos:
            self.tablaClients.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6],p[7],p[8],p[9],p[10]))

    def mostrarArtDesactivados(self):
        self.tablaClients.delete(*self.tablaClients.get_children())
        permisos_desactivados = clientesDesactivados()
        for p in permisos_desactivados:
            self.tablaClients.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))

    def update_art_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_clients.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM Clients WHERE
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
        for p in self.ListaClient:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaClients.delete(*self.tablaClients.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaClients.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()
        
    def crear_cliente(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateArt = customtkinter.CTkToplevel()
        self.topCreateArt.title("Nuevo Client")
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
        marco_crearclients = customtkinter.CTkFrame(self.topCreateArt, width=550,height=550, bg_color="white", fg_color="white")
        marco_crearclients.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(marco_crearclients, 0.8)
        self.lblinfo = customtkinter.CTkLabel(marco_crearclients, text="Registro de Client", font=("Roboto",14))
        self.lblinfo.place(relx=0.36, rely=0.04)
        #LINEA 1
        #Codigo del Client 1.1
        self.lblcodClient = customtkinter.CTkLabel(marco_crearclients, text='Codigo Client', font=("Roboto", 13))
        self.lblcodClient.place(x=55, y=60)

        self.svcodClient = customtkinter.StringVar()
        self.entrycodClient = ttk.Entry(marco_crearclients, style='Modern.TEntry', textvariable=self.svcodClient)
        self.entrycodClient.place(x=45, y=90)
        self.entrycodClient.configure(style='Entry.TEntry')

        #Nombre del cliente 1.2
        self.lblnombClient = customtkinter.CTkLabel(marco_crearclients, text='Nombre del Client', font=("Roboto", 13))
        self.lblnombClient.place(x=202, y=60)

        self.svnombClient = customtkinter.StringVar()
        self.entrynombClient = ttk.Entry(marco_crearclients, style='Modern.TEntry', textvariable=self.svnombClient)
        self.entrynombClient.place(x=200, y=90)
        self.entrynombClient.configure(style='Entry.TEntry')

        
        self.buttonGuardarArt = tk.Button(marco_crearclients, text="Guardar Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.GuardarClient())
        self.buttonGuardarArt.place(x=200, y=450)

    def GuardarClient(self):
        try:
            # Otener el contenido del Entry
            codart = buscarCorrelativo('cliente')
            codart = codart + 1
            fecha_actual = datetime.datetime.now()
            date_created = fecha_actual.strftime("%d/%m/%Y")
            date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")

            clients = Client(
                self.svcodClient.get(),
                self.svdepositos_var.get(),
                self.svcategoria_var.get(),
                self.svproveedor_var.get(),
                self.svnombClient.get(),
                self.svmarcaClient.get(),
                self.svmodeloClient.get(),
                self.svserialClient.get(),
                self.svcostoClient.get(),
                self.descripcionProd.get("1.0", "end-1c"),
                date_created,
                date_update
            )
            
            if self.id is None:
                save_client(clients)
                actualizarCorrelativo('cliente')

                self.topCreateArt.destroy()
            else:
                edit_client(clients, self.id)
                self.topEditArt.destroy()

            self.listarClientsEnTabla()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarClient, form_clients: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                
    def listarClientsEnTabla(self, where=None):
        try:
        # Limpiar la tabla existente
            self.tablaClients.delete(*self.tablaClients.get_children())

            if where is not None and len(where) > 0:
                self.ListaClient = searchClients(where)
            else:
                self.ListaClient = listClient()
                self.ListaClient.reverse()

            for p in self.ListaClient:
                self.tablaClients.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en listarClientsEnTabla, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            
    def editar_cliente(self, permisos, values):
        #Creacion del top level
        if values:
            self.id = self.tablaClients.item(self.tablaClients.selection())['text']
            self.editarcodClient = self.tablaClients.item(self.tablaClients.selection())['values'][0]
            self.editarnombClient = self.tablaClients.item(self.tablaClients.selection())['values'][4]
            self.editarproveedor = self.tablaClients.item(self.tablaClients.selection())['values'][3]
            self.editarmarcaClient = self.tablaClients.item(self.tablaClients.selection())['values'][5]
            self.editarmodeloClient = self.tablaClients.item(self.tablaClients.selection())['values'][6]
            self.editarserialClient = self.tablaClients.item(self.tablaClients.selection())['values'][7]
            self.editarcostoClient = self.tablaClients.item(self.tablaClients.selection())['values'][8]
            self.editarcategoria_var = self.tablaClients.item(self.tablaClients.selection())['values'][2]
            self.editardepositos_var = self.tablaClients.item(self.tablaClients.selection())['values'][1]
            self.editardescripcionProd = self.tablaClients.item(self.tablaClients.selection())['values'][9]
            
            
            self.topEditArt = customtkinter.CTkToplevel()
            self.topEditArt.title("Editar Client")
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
            marco_editarclients = customtkinter.CTkFrame(self.topEditArt, width=550,height=550, bg_color="white", fg_color="white")
            marco_editarclients.place(relx=0.5, rely=0.5, anchor="center")
            set_opacity(marco_editarclients, 0.8)
            self.lblinfo = customtkinter.CTkLabel(marco_editarclients, text="Registro de Client", font=("Roboto",14))
            self.lblinfo.place(relx=0.36, rely=0.04)
            #LINEA 1
            #Codigo del Client 1.1
            self.lblcodClient = customtkinter.CTkLabel(marco_editarclients, text='Codigo Client', font=("Roboto", 13))
            self.lblcodClient.place(x=55, y=60)

            self.svcodClient = customtkinter.StringVar(value=self.editarcodClient)
            self.entrycodClient = ttk.Entry(marco_editarclients, style='Modern.TEntry', textvariable=self.svcodClient)
            self.entrycodClient.place(x=45, y=90)
            self.entrycodClient.configure(style='Entry.TEntry')

            #Nombre del cliente 1.2
            self.lblnombClient = customtkinter.CTkLabel(marco_editarclients, text='Nombre del Client', font=("Roboto", 13))
            self.lblnombClient.place(x=202, y=60)

            self.svnombClient = customtkinter.StringVar(value=self.editarnombClient)
            self.entrynombClient = ttk.Entry(marco_editarclients, style='Modern.TEntry', textvariable=self.svnombClient)
            self.entrynombClient.place(x=200, y=90)
            self.entrynombClient.configure(style='Entry.TEntry')

            self.buttonActualizarArt = tk.Button(marco_editarclients, text="Actualizar Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.GuardarClient())
            self.buttonActualizarArt.place(x=200, y=450)

        else:
            messagebox.showerror("Error", "Debe seleccionar un modulo")

    def desactivarClient(self, permisos):
        try:
            self.id = self.tablaClients.item(self.tablaClients.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este cliente?")
            if confirmar:
                clientDelete(self.id)
                self.listarClientsEnTabla()
        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarClient, form_clients: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

