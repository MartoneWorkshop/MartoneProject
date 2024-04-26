import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL
import customtkinter
from customtkinter import CTkFont
from functions.ClientsDao import Clients, SaveClient, listarCliente, client_Delete, consulClient, EditClient
from config import COLOR_BOTON_CURSOR_ENCIMA, COLOR_BOTON_CURSOR_FUERA, COLOR_FG, COLOR_TEXTO, COLOR_HOVER
from tkinter import Image, ttk, messagebox, Canvas
import PIL 
from PIL import ImageTk, Image, ImageDraw
import sqlite3





class FormularioRegistrosDesign():

    def __init__(self, cuerpo_principal, logo):
        #STYLE INPUTS
        style = ttk.Style()
        style.configure('Entry.TEntry', background='white', foreground='black')

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(cuerpo_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        #self.labelTitulo = tk.Label(
        #    self.barra_superior, text="SECCION REGISTROS")
        #self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        #self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Segundo Label con la imagen
        self.label_imagen = tk.Label(self.barra_inferior, image=logo)
        self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_CUERPO_PRINCIPAL)

        ############################################ INICIO DE LABELS ###################################################
        #self.logo_img = customtkinter.CTkImage(Image.open("imagenes/logo.png"), size=(300,300))
        #self.lblLogo = customtkinter.CTkLabel(cuerpo_principal, image=self.logo_img, text="", fg_color='transparent', bg_color='transparent')
        #self.lblLogo.place(x=700, y=15)
        ###################################################     1       #################################################    
        #Label del Nombre
        self.lblclient_firstname = customtkinter.CTkLabel(cuerpo_principal, text='Nombre:', font=("Roboto", 14))
        self.lblclient_firstname.place(x=50, y=30)
        #Entry del Nombre
        self.svclient_firstname = customtkinter.StringVar()
        self.entryclient_firstname = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry', textvariable=self.svclient_firstname)
        self.entryclient_firstname.place(x=50, y=55)
        self.entryclient_firstname.configure(style='Entry.TEntry')
        
        ###################################################     2       #################################################  
        #Label del Apellido
        self.lblclient_lastname = customtkinter.CTkLabel(cuerpo_principal, text='Apellido:', font=("Roboto", 14))
        self.lblclient_lastname.place(x=365, y=30)
        #Entry del Apellido
        self.svclient_lastname = customtkinter.StringVar()
        self.entryclient_lastname = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry', textvariable=self.svclient_lastname)
        self.entryclient_lastname.place(x=365, y=55)
        self.entryclient_lastname.configure(style='Entry.TEntry')

        #self.entryclient_lastname = customtkinter.CTkEntry(cuerpo_principal, textvariable=self.svclient_lastname, width=200)
        #self.entryclient_lastname.place(x=365, y=55)

        ###################################################     3         #################################################
        self.lblclient_ci = customtkinter.CTkLabel(cuerpo_principal, text='Cedula:', font=("Roboto", 14))
        self.lblclient_ci.place(x=50, y=125)
        #Entry de la Cedula
        self.svclient_ci = customtkinter.StringVar()
        self.entryclient_ci = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry', textvariable=self.svclient_ci)
        self.entryclient_ci.place(x=50, y=155)
        self.entryclient_ci.configure(style='Entry.TEntry')
        self.entryclient_ci.bind('<KeyRelease>', self.check_entry_content)
        #Status Label
        self.status_label = tk.Label(cuerpo_principal)
        self.status_label.place(x=260, y=150)

        ###################################################     4       #################################################  
        #Label del Correo
        self.lblclient_mail = customtkinter.CTkLabel(cuerpo_principal, text='Correo:', font=("Roboto", 14))
        self.lblclient_mail.place(x=365, y=125)
        #Entry del Correo
        self.svclient_mail = customtkinter.StringVar()
        self.entryclient_mail = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry', textvariable=self.svclient_mail)
        self.entryclient_mail.place(x=365, y=150)
        self.entryclient_mail.configure(style='Entry.TEntry')

        ###################################################     5       #################################################  
        #Label del Telefono
        self.lblclient_phone = customtkinter.CTkLabel(cuerpo_principal, text='NºTelefono:', font=("Roboto", 14))
        self.lblclient_phone.place(x=50, y=225)

        #Entry del Telefono
        self.svclient_phone = customtkinter.StringVar()
        self.entryclient_phone = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry', textvariable=self.svclient_phone)
        self.entryclient_phone.place(x=50, y=250)
        self.entryclient_phone.configure(style='Entry.TEntry')

        ###################################################     6       #################################################  
            
        #Label de la Direccion
        self.lblclient_address = customtkinter.CTkLabel(cuerpo_principal, text='Direccion:', font=("Roboto", 14))
        self.lblclient_address.place(x=365, y=225)

        #Entry de la Direccion
        self.svclient_address = customtkinter.StringVar()
        self.entryclient_address = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry', textvariable=self.svclient_address)
        self.entryclient_address.place(x=365, y=250)
        self.entryclient_address.configure(style='Entry.TEntry')
        self.entryclient_address.bind("<Return>", lambda event: self.GuardarCliente())

        #TESTING ZONE

        #style = ttk.Style()
        #style.configure('Entry.TEntry', background='white', foreground='black')
        ## Crear el Entry utilizando ttk.Entry
        #self.entryTEST = ttk.Entry(cuerpo_principal, width=30, style='Modern.TEntry')
        #self.entryTEST.place(x=605, y=250)
        #self.entryTEST.configure(style='Entry.TEntry')
        
        
        ######################################### FIN DE ENTRYS Y LABELS ####################################################
    
        ################################################ BOTONES DE EDITAR Y ELIMINAR ##################################################
        self.buttonSave_client_img = customtkinter.CTkImage(Image.open("imagenes/user_save-white.png"))
        self.buttonSave_client = customtkinter.CTkButton(cuerpo_principal, image=self.buttonSave_client_img, text="Guardar", font=("Roboto", 18), 
        width=50, height=40, corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER, command=self.GuardarCliente)
        self.buttonSave_client.place(x=70, y=350)

        self.buttonEdit_client_img = customtkinter.CTkImage(Image.open("imagenes/user_edit-white.png"))
        self.buttonEdit_client = customtkinter.CTkButton(cuerpo_principal, image=self.buttonEdit_client_img, text="Editar", font=("Roboto", 18), 
        width=50, height=40,  corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER, command=self.editarCliente)
        self.buttonEdit_client.place(x=240, y=400)
    
        self.buttonDelete_client_img = customtkinter.CTkImage(Image.open("imagenes/user_delete-white.png"))
        self.buttonDelete_client = customtkinter.CTkButton(cuerpo_principal, image=self.buttonDelete_client_img, text="Eliminar", font=("Roboto", 18), 
        width=50, height=40,  corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER, command=self.eliminarCliente)
        self.buttonDelete_client.place(x=380, y=400)
        
        self.buttonClean_img = customtkinter.CTkImage(Image.open("imagenes/delete-white.png"))
        self.buttonClean = customtkinter.CTkButton(cuerpo_principal, image=self.buttonClean_img, text="Limpiar", font=("Roboto", 18),
        width=50, height=40,  corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER,command=self.Depurador)
        self.buttonClean.place(x=520, y=400)
        
        ####################################################### ENTRY DE BUSQUEDA #######################################################
        self.lblsearch_clients = customtkinter.CTkLabel(cuerpo_principal, text='Buscar:', fg_color="#dbdbdb", bg_color="#dbdbdb")
        self.lblsearch_clients.place(x=915, y=542)
        self.sventrysearch_clients = customtkinter.StringVar()
        self.entrysearch_clients = customtkinter.CTkEntry(cuerpo_principal, textvariable=self.sventrysearch_clients, bg_color="#dbdbdb", width=150)
        self.entrysearch_clients.place(x=967, y=542)
        self.entrysearch_clients.bind('<KeyRelease>', self.update_client_content)

        where = ""
        #################################################### INFORMACION DE LA TABLA ####################################################
        if len(where) > 0:
            self.listaCliente = consulClient(where)
        else:
            self.listaCliente = listarCliente()
            self.listaCliente.reverse()

        self.tablaClientes = ttk.Treeview(cuerpo_principal, column=('client_firstname','client_lastname','client_ci','client_phone','client_address','client_mail'))
        self.tablaClientes.place(x=70, y=580)
        self.scroll = ttk.Scrollbar(cuerpo_principal, orient='vertical', command=self.tablaClientes.yview)
        self.scroll.place(x=1118, y=250, height=225)
        self.tablaClientes.configure(yscrollcommand=self.scroll.set)
        self.tablaClientes.tag_configure('evenrow')
        self.tablaClientes.heading('#0',text="ID")
        self.tablaClientes.heading('#1',text="NOMBRE")
        self.tablaClientes.heading('#2',text="APELLIDO")
        self.tablaClientes.heading('#3',text="CEDULA")
        self.tablaClientes.heading('#4',text="TELEFONO")
        self.tablaClientes.heading('#5',text="DIRECCION")
        self.tablaClientes.heading('#6',text="CORREO")
        self.tablaClientes.column("#0", width=45, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaClientes.column("#1", width=125, stretch=False)
        self.tablaClientes.column("#2", width=125, stretch=False)
        self.tablaClientes.column("#3", width=125, stretch=False)
        self.tablaClientes.column("#4", width=125, stretch=False)
        self.tablaClientes.column("#5", width=250, stretch=False)
        self.tablaClientes.column("#6", width=250, stretch=False)
    
        for p in self.listaCliente:
            self.tablaClientes.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6]))
    def check_entry_content(self, event=None):
        # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
        # Obtener el contenido del Entry
        self.content = self.entryclient_ci.get()
        # Realizar la consulta
        self.cursor.execute("SELECT * FROM Clients WHERE client_ci = ?", (self.content,))
        self.result = self.cursor.fetchone()

    # Verificar si el contenido ya existe
        if self.result:
            self.wrong_image = Image.open("imagenes/wrong.png")
            self.wrong_image = self.wrong_image.resize((25,25),Image.BILINEAR)
            self.wrong_photo = ImageTk.PhotoImage(self.wrong_image)
            self.status_label.configure(image=self.wrong_photo)
            self.status_label.image = self.wrong_photo
        else:
            correct_image = Image.open("imagenes/correct.png")
            correct_image = correct_image.resize((25,25), Image.BILINEAR)
            correct_photo= ImageTk.PhotoImage(correct_image)
            self.status_label.configure(image=correct_photo)
            self.status_label.image = correct_photo
        self.cursor.close()
        self.connection.close()

    def update_client_content(self, event=None):
    # Conectar a la base de datos
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()
    # Obtener el contenido del Entry
        self.content = self.entrysearch_clients.get()
    # Realizar la consulta
        self.cursor.execute("""SELECT * FROM Clients WHERE
                        id_client LIKE ? OR 
                        client_firstname LIKE ? OR 
                        client_lastname LIKE ? OR 
                        client_ci LIKE ? OR 
                        client_phone LIKE ? OR 
                        client_address LIKE ? OR
                        client_mail LIKE ?""", 
                        ('%' + self.content + '%',
                        '%' + self.content + '%',  
                        '%' + self.content + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%',
                        '%' + self.content.strip() + '%', 
                        '%' + self.content.strip() + '%'))
        self.result = self.cursor.fetchall()
    # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.listaCliente:
            if self.content.lower() in str(p[0]).lower() or self.content.lower() in str(p[1]).lower() or self.content.lower() in str(p[2]).lower() or self.content.lower() in str(p[3]).lower() or self.content.lower() in str(p[4]).lower() or self.content.lower() in str(p[5]).lower() or self.content.lower() in str(p[6]).lower():              filtered_results.append(p)

    # Borrar los elementos existentes en la tablaEquipos
        self.tablaClientes.delete(*self.tablaClientes.get_children())

    # Insertar los nuevos resultados en la tablaEquipos
        for p in filtered_results:
            self.tablaClientes.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))
        self.cursor.close()
        self.connection.close()

############################################################# FUNCIONES DE BOTONES ##############################################################
    def binding_hover_buttons_event(self, button):
        button.bind("<Enter>", lambda event: self.buttons_on_enter(event, button))
        button.bind("<Leave>", lambda event: self.buttons_on_leave(event, button))

    def buttons_on_enter(self, event, button):
        button.configure(bg_color=COLOR_BOTON_CURSOR_ENCIMA, fg_color='transparent')

    def buttons_on_leave(self, event, button):
        button.configure(fg_color='transparent', bg_color='transparent')

    def GuardarCliente(self):
        clients = Clients(
            self.svclient_firstname.get(),
            self.svclient_lastname.get(),
            self.svclient_ci.get(),
            self.svclient_phone.get(),
            self.svclient_address.get(),
            self.svclient_mail.get()
        )

        if self.id_client is None:
            SaveClient(clients)
        else:
            EditClient(clients, self.id_client)
        self.Depurador()
        self.listarClientesEnTabla()
    
    def eliminarCliente(self):
        try:
            self.id_client = self.tablaClientes.item(self.tablaClientes.selection())['text']
            client_Delete(self.id_client)
            
            self.listarClientesEnTabla()
            self.id_client = None

        except Exception as e:
            title = 'Error de Sistema'
            mensaje = f'Error en EliminarCliente: {str(e)}'
            messagebox.showerror = (title, mensaje) 
        
    def listarClientesEnTabla(self, where=None):
    # Limpiar la tabla existente
        self.tablaClientes.delete(*self.tablaClientes.get_children())

        if where is not None and len(where) > 0:
            self.listaCliente = consulClient(where)
        else:
            self.listaCliente = listarCliente()
            self.listaCliente.reverse()

        for p in self.listaCliente:
            self.tablaClientes.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))

    def editarCliente(self):
        try:
            self.Depurador()
            self.id_client = self.tablaClientes.item(self.tablaClientes.selection())['text']
            self.client_firstname = self.tablaClientes.item(self.tablaClientes.selection())['values'][0]
            self.client_lastname = self.tablaClientes.item(self.tablaClientes.selection())['values'][1]
            self.client_ci = self.tablaClientes.item(self.tablaClientes.selection())['values'][2]
            self.client_phone = self.tablaClientes.item(self.tablaClientes.selection())['values'][3]
            self.client_address = self.tablaClientes.item(self.tablaClientes.selection())['values'][4]
            self.client_mail = self.tablaClientes.item(self.tablaClientes.selection())['values'][5]

            self.entryclient_firstname.insert(0, self.client_firstname)
            self.entryclient_lastname.insert(0, self.client_lastname)
            self.entryclient_ci.insert(0, self.client_ci)
            self.entryclient_phone.insert(0, self.client_phone)
            self.entryclient_address.insert(0, self.client_address)
            self.entryclient_mail.insert(0, self.client_mail)

        except Exception as e:
            title = 'Error de Sistema'
            mensaje = f'Error editarCliente: {str(e)}'
            messagebox.showerror(title, mensaje) 

    def Depurador(self):
        self.svclient_firstname.set('')
        self.svclient_lastname.set('')
        self.svclient_ci.set('')
        self.svclient_phone.set('')
        self.svclient_address.set('')
        self.svclient_mail.set('')