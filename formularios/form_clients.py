import tkinter as tk
from config import  COLOR_FONDO
import PIL
import sqlite3
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
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

        self.frame_clients = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.frame_clients.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.frame_clients, 0.8)
        ##################################################### BOTONES DE LA TABLA ##################################################
        self.buttonCreateClient = tk.Button(self.frame_clients, text="Crear\n Client", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.FormCreateClient(permisos))
        self.buttonCreateClient.place(x=140, y=50)

        self.buttonEditClient = tk.Button(self.frame_clients, text="Editar\n Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.FormEditClient(permisos, self.clientsTable.item(self.clientsTable.selection())['values']))
        self.buttonEditClient.place(x=265, y=50)
            
        self.buttonDeleteClient = tk.Button(self.frame_clients, text="Desactivar\n Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.inactivateClient(permisos))
        self.buttonDeleteClient.place(x=390, y=50)

        #Switch de activos/inactivos
        self.switchStatus = tk.BooleanVar(value=True)
        self.switchClientStatus = customtkinter.CTkSwitch(self.frame_clients, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=self.showStatus)
        self.switchClientStatus.place(x=900, y=157)

        ###################################################### BUSCADOR DE LA TABLA #################################################
        search_image = Image.open("imagenes/icons/search.png")
        search_resized = search_image.resize((WIDTH_LOGO, HEIGHT_LOGO))
        self.search_icon = ImageTk.PhotoImage(search_resized)
        self.lblsearch_clients = customtkinter.CTkLabel(self.frame_clients, text='', image=self.search_icon, font=("Roboto", 14))
        self.lblsearch_clients.place(x=65, y=155)

        self.sventrysearch_clients = customtkinter.StringVar()
        self.entrysearch_clients = ttk.Entry(self.frame_clients, textvariable=self.sventrysearch_clients, style='Modern.TEntry', width=30)
        self.entrysearch_clients.place(x=100, y=157)
        self.entrysearch_clients.bind('<KeyRelease>', self.updateSearch)

        #################################################### INFORMACION DE LA TABLA ####################################################
        where = ""
        if len(where) > 0:
            self.clientList = searchClients(where)
        else:            
            self.clientList = listClient()
            self.clientList.reverse()

        self.clientsTable = ttk.Treeview(self.frame_clients, column=('client_firstname','client_lastname','client_ci',
                                                                     'client_phone','client_address','client_email','created_at'), height=25)
        self.clientsTable.place(x=32, y=200)

        self.scroll = ttk.Scrollbar(self.frame_clients, orient='vertical', command=self.clientsTable.yview)
        self.scroll.place(x=1084, y=200, height=526)

        self.clientsTable.configure(yscrollcommand=self.scroll.set)
        self.clientsTable.tag_configure('evenrow')

        self.clientsTable.heading('#0',text="ID" )
        self.clientsTable.heading('#1',text="Nombre")
        self.clientsTable.heading('#2',text="Apellido")
        self.clientsTable.heading('#3',text="Documento")
        self.clientsTable.heading('#4',text="Telefono")
        self.clientsTable.heading('#5',text="Direccion")
        self.clientsTable.heading('#6',text="Correo")
        self.clientsTable.heading('#7',text="Creado en")

        self.clientsTable.column("#0", width=50, stretch=True, anchor='w')
        self.clientsTable.column("#1", width=100, stretch=True)
        self.clientsTable.column("#2", width=100, stretch=True)
        self.clientsTable.column("#3", width=100, stretch=True)
        self.clientsTable.column("#4", width=100, stretch=True)
        self.clientsTable.column("#5", width=100, stretch=True)
        self.clientsTable.column("#6", width=100, stretch=True)
        self.clientsTable.column("#7", width=100, stretch=True)


        for p in self.clientList:
            self.clientsTable.insert('','end',iid=p[0], text=p[0],values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7]))

        self.clientsTable.bind('<Double-1>', lambda event: self.FormEditClient(event, self.clientsTable.item(self.clientsTable.selection())['values']))

    def showStatus(self):
        if self.switchStatus.get():
            self.switchClientStatus.configure(text="Activos")
            self.showActive()
        else:
            self.switchClientStatus.configure(text="Inactivos")
            self.showInactive()
     
    def showActive(self):
        # Borrar los elementos existentes en la tabla de permisos
        self.clientsTable.delete(*self.clientsTable.get_children())
        # Obtener la lista de permisos activos
        clientes_activos = listClient()
        # Insertar los permisos activos en la tabla
        for p in clientes_activos:
            self.clientsTable.insert('', 0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7]))

    def showInactive(self):
        self.clientsTable.delete(*self.clientsTable.get_children())
        permisos_desactivados = clientesDesactivados()
        for p in permisos_desactivados:
            self.clientsTable.insert('',0, text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7]))

    def updateSearch(self, event=None):
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
        for p in self.clientList:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower():              
                filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.clientsTable.delete(*self.clientsTable.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.clientsTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
        self.cursor.close()
        self.connection.close()
        
    def FormCreateClient(self, permisos):
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
        frame_createClient = customtkinter.CTkFrame(self.topCreateArt, width=550,height=550, bg_color="white", fg_color="white")
        frame_createClient.place(relx=0.5, rely=0.5, anchor="center")
        set_opacity(frame_createClient, 0.8)
        self.lblinfo = customtkinter.CTkLabel(frame_createClient, text="Registro de Client", font=("Roboto",14))
        self.lblinfo.place(relx=0.36, rely=0.04)
        #LINEA 1
        #Codigo del Client 1.1
        self.lblcodClient = customtkinter.CTkLabel(frame_createClient, text='Codigo Client', font=("Roboto", 13))
        self.lblcodClient.place(x=55, y=60)

        self.svcodClient = customtkinter.StringVar()
        self.entrycodClient = ttk.Entry(frame_createClient, style='Modern.TEntry', textvariable=self.svcodClient)
        self.entrycodClient.place(x=45, y=90)
        self.entrycodClient.configure(style='Entry.TEntry')

        #Nombre del cliente 1.2
        self.lblnombClient = customtkinter.CTkLabel(frame_createClient, text='Nombre del Client', font=("Roboto", 13))
        self.lblnombClient.place(x=202, y=60)

        self.svnombClient = customtkinter.StringVar()
        self.entrynombClient = ttk.Entry(frame_createClient, style='Modern.TEntry', textvariable=self.svnombClient)
        self.entrynombClient.place(x=200, y=90)
        self.entrynombClient.configure(style='Entry.TEntry')

        
        self.buttonGuardarArt = tk.Button(frame_createClient, text="Guardar Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                            command=lambda: self.SaveClient())
        self.buttonGuardarArt.place(x=200, y=450)

    def SaveClient(self):
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

            self.updateTable()
            
        except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarClient, form_clients: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                
    def updateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.clientsTable.delete(*self.clientsTable.get_children())

            if where is not None and len(where) > 0:
                self.clientList = searchClients(where)
            else:
                self.clientList = listClient()
                self.clientList.reverse()

            for p in self.clientList:
                self.clientsTable.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
        except Exception as e:
            error_advice()
            mensaje = f'Error en updateTable, form_users: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
            
    def FormEditClient(self, permisos, values):
        #Creacion del top level
        if values:
            self.id = self.clientsTable.item(self.clientsTable.selection())['text']
            self.editarcodClient = self.clientsTable.item(self.clientsTable.selection())['values'][0]
            self.editarnombClient = self.clientsTable.item(self.clientsTable.selection())['values'][4]
            self.editarproveedor = self.clientsTable.item(self.clientsTable.selection())['values'][3]
            self.editarmarcaClient = self.clientsTable.item(self.clientsTable.selection())['values'][5]
            self.editarmodeloClient = self.clientsTable.item(self.clientsTable.selection())['values'][6]
            self.editarserialClient = self.clientsTable.item(self.clientsTable.selection())['values'][7]
            self.editarcostoClient = self.clientsTable.item(self.clientsTable.selection())['values'][8]
            self.editarcategoria_var = self.clientsTable.item(self.clientsTable.selection())['values'][2]
            self.editardepositos_var = self.clientsTable.item(self.clientsTable.selection())['values'][1]
            self.editardescripcionProd = self.clientsTable.item(self.clientsTable.selection())['values'][9]
            
            
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
            frame_editClient = customtkinter.CTkFrame(self.topEditArt, width=550,height=550, bg_color="white", fg_color="white")
            frame_editClient.place(relx=0.5, rely=0.5, anchor="center")
            set_opacity(frame_editClient, 0.8)
            self.lblinfo = customtkinter.CTkLabel(frame_editClient, text="Registro de Client", font=("Roboto",14))
            self.lblinfo.place(relx=0.36, rely=0.04)
            #LINEA 1
            #Codigo del Client 1.1
            self.lblcodClient = customtkinter.CTkLabel(frame_editClient, text='Codigo Client', font=("Roboto", 13))
            self.lblcodClient.place(x=55, y=60)

            self.svcodClient = customtkinter.StringVar(value=self.editarcodClient)
            self.entrycodClient = ttk.Entry(frame_editClient, style='Modern.TEntry', textvariable=self.svcodClient)
            self.entrycodClient.place(x=45, y=90)
            self.entrycodClient.configure(style='Entry.TEntry')

            #Nombre del cliente 1.2
            self.lblnombClient = customtkinter.CTkLabel(frame_editClient, text='Nombre del Client', font=("Roboto", 13))
            self.lblnombClient.place(x=202, y=60)

            self.svnombClient = customtkinter.StringVar(value=self.editarnombClient)
            self.entrynombClient = ttk.Entry(frame_editClient, style='Modern.TEntry', textvariable=self.svnombClient)
            self.entrynombClient.place(x=200, y=90)
            self.entrynombClient.configure(style='Entry.TEntry')

            self.buttonActualizarArt = tk.Button(frame_editClient, text="Actualizar Client", font=("Roboto", 12), state='normal', bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                                command=lambda: self.SaveClient())
            self.buttonActualizarArt.place(x=200, y=450)

        else:
            messagebox.showerror("Error", "Debe seleccionar un modulo")

    def inactivateClient(self, permisos):
        try:
            self.id = self.clientsTable.item(self.clientsTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desactivar este cliente?")
            if confirmar:
                clientDelete(self.id)
                self.updateTable()
        except Exception as e:
            error_advice()
            mensaje = f'Error en inactivateClient, form_clients: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

