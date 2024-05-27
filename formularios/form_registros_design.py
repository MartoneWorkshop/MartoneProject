import tkinter as tk
from config import  COLOR_FONDO
import customtkinter
from customtkinter import CTkFont
from functions.ClientsDao import Clients, SaveClient, listarCliente, client_Delete, consulClient, EditClient
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice    
from config import COLOR_BOTON_CURSOR_ENCIMA, COLOR_MENU_LATERAL, COLOR_BOTON_CURSOR_FUERA, COLOR_FG, COLOR_TEXTO, COLOR_HOVER
from tkinter import Image, ttk, messagebox, Canvas
import PIL
import util.util_imagenes as util_img 
from PIL import ImageTk, Image, ImageDraw, ImageGrab
import sqlite3


class FormularioRegistrosDesign():
    
    def __init__(self, cuerpo_principal, width_screen, height_screen):
        self.width_screen = width_screen
        self.height_screen = height_screen
        self.id_client = None
        self.cuerpo_principal = cuerpo_principal
        self.cuerpo_principal.bind('<Configure>', self.on_resize)
        self.original_width = 1120
        self.original_height = 800
        
        #STYLE INPUTS
        style = ttk.Style()
        style.configure('Entry.TEntry', foreground='black')

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Crear paneles: barra inferiorw
        self.panel_principal = tk.Frame(cuerpo_principal, bg="white")
        self.panel_principal.pack(side=tk.BOTTOM, fill='both', expand=True)    
        
        self.marco_principal = customtkinter.CTkFrame(cuerpo_principal, fg_color="red", width=1120, height=800)
        self.marco_principal.place(relx=0.5, rely=0.5, anchor="center")

        
        ###############################################################################
        ############# INICIALIZACION DE LA IMAGEN DE FONDO AUTOEXPANDIBLE #############
        #ruta_imagen = "imagenes/bg.jpg"
        ## Cargar la imagen
        #imagen = Image.open(ruta_imagen)
        #imagen_tk = ImageTk.PhotoImage(imagen)
        #self.imagen_tk = imagen_tk
        ## Crear el Label con la imagen de fondo
        #label_fondo = tk.Label(cuerpo_principal, image=imagen_tk)
        #label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        #self.label_fondo = label_fondo
        ## Configurar el Label para que se ajuste automáticamente al tamaño del frame
        #def ajustar_imagen(event):
        #    # Cambiar el tamaño de la imagen para que coincida con el tamaño del frame
        #    nueva_imagen = imagen.resize((event.width, event.height))
        #    nueva_imagen_tk = ImageTk.PhotoImage(nueva_imagen)
        #    self.imagen_tk = nueva_imagen_tk
        #    # Actualizar la imagen en el Label de fondo
        #    label_fondo.config(image=nueva_imagen_tk)
        #
        #cuerpo_principal.bind("<Configure>", ajustar_imagen)

        
        ###############################################################################

        ###################################################     1       #################################################    
        
        #Label del Nombre bg_color="#e2e2e2",
        marco_firstname = customtkinter.CTkFrame(self.marco_principal, width=225, height=55)
        marco_firstname.place(x=50, y=50)

        self.lblclient_firstname = customtkinter.CTkLabel(marco_firstname, text='Nombre:', font=("Roboto", 14), compound='center')
        self.lblclient_firstname.place(x=5, y=1)
        #Entry del Nombre
        self.svclient_firstname = customtkinter.StringVar()
        self.entryclient_firstname = ttk.Entry(marco_firstname, width=30, style='Modern.TEntry', textvariable=self.svclient_firstname)
        self.entryclient_firstname.place(x=5, y=25)
        self.entryclient_firstname.configure(style='Entry.TEntry')
        
        ###################################################     2       #################################################  
        #MARCO
        marco_lastname = customtkinter.CTkFrame(self.marco_principal, width=225, height=55)
        marco_lastname.place(x=405, y=50)
        #Label del Apellido
        self.lblclient_lastname = customtkinter.CTkLabel(marco_lastname, text='Apellido:', font=("Roboto", 14))
        self.lblclient_lastname.place(x=5, y=1)
        #Entry del Apellido
        self.svclient_lastname = customtkinter.StringVar()
        self.entryclient_lastname = ttk.Entry(marco_lastname, width=30, style='Modern.TEntry', textvariable=self.svclient_lastname)
        self.entryclient_lastname.place(x=5, y=25)
        self.entryclient_lastname.configure(style='Entry.TEntry')
        ###################################################     3         #################################################
        # Configurar el estilo para el marco
        marco_cedula = customtkinter.CTkFrame(self.marco_principal, width=225, height=55)
        marco_cedula.place(x=50, y=150)

        # Cargar la imagen de fondo
        self.lblclient_ci = customtkinter.CTkLabel(marco_cedula, text='Cedula:', font=("Roboto", 14))
        self.lblclient_ci.place(x=5, y=1)
        
        #Entry de la Cedula
        self.svclient_ci = customtkinter.StringVar()
        self.entryclient_ci = ttk.Entry(marco_cedula, width=30, style='Modern.TEntry', textvariable=self.svclient_ci)
        self.entryclient_ci.place(x=5, y=25)
        self.entryclient_ci.configure(style='Entry.TEntry')
        self.entryclient_ci.bind('<KeyRelease>', self.check_entry_content)
        #Status Label
        self.status_label = tk.Label(marco_cedula, bg="#dbdbdb")
        self.status_label.place(x=194, y=20)

        ###################################################     4       #################################################  
        #MARCO       
        marco_mail = customtkinter.CTkFrame(self.marco_principal, width=225, height=55)
        marco_mail.place(x=405, y=150)
        #Label del Correo
        self.lblclient_mail = customtkinter.CTkLabel(marco_mail, text='Correo:', font=("Roboto", 14))
        self.lblclient_mail.place(x=5, y=1)
        #Entry del Correo
        self.svclient_mail = customtkinter.StringVar()
        self.entryclient_mail = ttk.Entry(marco_mail, width=30, style='Modern.TEntry', textvariable=self.svclient_mail)
        self.entryclient_mail.place(x=5, y=25)
        self.entryclient_mail.configure(style='Entry.TEntry')

        ###################################################     5       #################################################  
        #MARCO
        marco_phone = customtkinter.CTkFrame(self.marco_principal, width=225, height=55)
        marco_phone.place(x=50, y=255)
        #Label del Telefono
        self.lblclient_phone = customtkinter.CTkLabel(marco_phone, text='NºTelefono:', font=("Roboto", 14))
        self.lblclient_phone.place(x=5, y=1)

        #Entry del Telefono
        self.svclient_phone = customtkinter.StringVar()
        self.entryclient_phone = ttk.Entry(marco_phone, width=30, style='Modern.TEntry', textvariable=self.svclient_phone)
        self.entryclient_phone.place(x=5, y=25)
        self.entryclient_phone.configure(style='Entry.TEntry')

        ###################################################     6       #################################################  
        #MARCO
        marco_address = customtkinter.CTkFrame(self.marco_principal, width=225, height=55)
        marco_address.place(x=405, y=255)
        #Label de la Direccion
        self.lblclient_address = customtkinter.CTkLabel(marco_address, text='Direccion:', font=("Roboto", 14))
        self.lblclient_address.place(x=5, y=1)

        #Entry de la Direccion
        self.svclient_address = customtkinter.StringVar()
        self.entryclient_address = ttk.Entry(marco_address, width=30, style='Modern.TEntry', textvariable=self.svclient_address)
        self.entryclient_address.place(x=5, y=25)
        self.entryclient_address.configure(style='Entry.TEntry')
        self.entryclient_address.bind("<Return>", lambda event: self.GuardarCliente())

        ######################################### FIN DE ENTRYS Y LABELS ####################################################
        ###TEST BUTTON ####
        #buttontest = tk.Button(cuerpo_principal, text="TEST", command=show_notification)
        #buttontest.place(x=200, y=500)
        marco_tabla = customtkinter.CTkFrame(self.marco_principal, width=1080, height=300, corner_radius=10)
        marco_tabla.place(x=22, y=480)
        ################################################ BOTONES DE EDITAR Y ELIMINAR ##################################################
        
        self.buttonSave_client_img = customtkinter.CTkImage(Image.open("imagenes/user_save-white.png"))
        self.buttonSave_client = customtkinter.CTkButton(marco_tabla, image=self.buttonSave_client_img, text="Guardar", font=("Roboto", 16), 
        width=50, height=40, corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER, command=self.GuardarCliente)
        self.buttonSave_client.place(x=15, y=10)

        self.buttonEdit_client_img = customtkinter.CTkImage(Image.open("imagenes/user_edit-white.png"))
        self.buttonEdit_client = customtkinter.CTkButton(marco_tabla, image=self.buttonEdit_client_img, text="Editar", font=("Roboto", 16), 
        width=50, height=40,  corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER, command=self.editarCliente)
        self.buttonEdit_client.place(x=190, y=10)
    
        self.buttonDelete_client_img = customtkinter.CTkImage(Image.open("imagenes/user_delete-white.png"))
        self.buttonDelete_client = customtkinter.CTkButton(marco_tabla, image=self.buttonDelete_client_img, text="Eliminar", font=("Roboto", 16), 
        width=50, height=40,  corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER, command=self.eliminarCliente)
        self.buttonDelete_client.place(x=345, y=10)
        
        self.buttonClean_img = customtkinter.CTkImage(Image.open("imagenes/delete-white.png"))
        self.buttonClean = customtkinter.CTkButton(marco_tabla, image=self.buttonClean_img, text="Limpiar", font=("Roboto", 16),
        width=50, height=40,  corner_radius=50, text_color=COLOR_TEXTO, fg_color=COLOR_FG, hover_color=COLOR_HOVER,command=self.Depurador)
        self.buttonClean.place(x=520, y=10)
        ####################################################### ENTRY DE BUSQUEDA #######################################################
        self.lblsearch_clients = customtkinter.CTkLabel(marco_tabla, text='Buscar:', fg_color="#dbdbdb", bg_color="#dbdbdb", font=("Roboto", 14))
        self.lblsearch_clients.place(x=810, y=17)

        self.sventrysearch_clients = customtkinter.StringVar()
        self.entrysearch_clients = ttk.Entry(marco_tabla, textvariable=self.sventrysearch_clients, style='Modern.TEntry', background="#dbdbdb", width=30)
        self.entrysearch_clients.place(x=870, y=20)
        self.entrysearch_clients.bind('<KeyRelease>', self.update_client_content)

        where = ""
        #################################################### INFORMACION DE LA TABLA ####################################################
        if len(where) > 0:
            self.listaCliente = consulClient(where)
        else:
            self.listaCliente = listarCliente()
            self.listaCliente.reverse()

        self.tablaClientes = ttk.Treeview(marco_tabla, column=('client_firstname','client_lastname','client_ci','client_phone','client_address','client_mail'))
        self.tablaClientes.place(x=10, y=60)
        self.scroll = ttk.Scrollbar(marco_tabla, orient='vertical', command=self.tablaClientes.yview)
        self.scroll.place(x=1057, y=60, height=225)
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
        

        self.marco_firstname = marco_firstname
        self.marco_lastname = marco_lastname
        self.marco_cedula = marco_cedula
        self.marco_address = marco_address
        self.marco_mail = marco_mail
        self.marco_phone = marco_phone
        self.marco_tabla = marco_tabla

    def call_resize(self, width_screen, height_screen):
        self.width_screen = width_screen
        self.height_screen = height_screen
        print(width_screen, height_screen)
        new_width = 1548
        new_height =  873.9
        # Coloca e l marco principal en las coordenadas calculadas para centrarlo
        self.marco_principal.configure(width=new_width, height=new_height)
        self.marco_principal.place(relx=0.5, rely=0.5)
        
        #Reubicacion de los marcos:
        #Marco firstname
        self.marco_firstname.configure(width=235, height=65)
        self.marco_firstname.place(x=110, y=50)
        self.lblclient_firstname.configure(font=("Roboto", 15))
        self.lblclient_firstname.place(x=5, y=7)
        self.entryclient_firstname.config(width=30)
        self.entryclient_firstname.place(x=5, y=33)
        #Marco lastname
        self.marco_lastname.configure(width=235, height=65)
        self.marco_lastname.place(x=465, y=50)
        self.lblclient_lastname.configure(font=("Roboto", 15))
        self.lblclient_lastname.place(x=5, y=7)
        self.entryclient_lastname.config(width=30)
        self.entryclient_lastname.place(x=5, y=33)
        #Marco cedula
        self.marco_cedula.configure(width=235, height=65)
        self.marco_cedula.place(x=110, y=150)
        self.lblclient_ci.configure(font=("Roboto", 15))
        self.lblclient_ci.place(x=5, y=7)
        self.entryclient_ci.config(width=30)
        self.entryclient_ci.place(x=5, y=33)
        #Marco mail 
        self.marco_mail.configure(width=235, height=65)
        self.marco_mail.place(x=465, y=150)
        self.lblclient_mail.configure(font=("Roboto", 15))
        self.lblclient_mail.place(x=5, y=7)
        self.entryclient_mail.config(width=30)
        self.entryclient_mail.place(x=5, y=33)
        #Marco address
        self.marco_address.configure(width=235, height=65)
        self.marco_address.place(x=465, y=255)
        self.lblclient_address.configure(font=("Roboto", 15))
        self.lblclient_address.place(x=5, y=7)
        self.entryclient_address.config(width=30)
        self.entryclient_address.place(x=5, y=33)
        #Marco phone
        self.marco_phone.configure(width=235, height=65)
        self.marco_phone.place(x=110, y=255)
        self.lblclient_phone.configure(font=("Roboto", 15))
        self.lblclient_phone.place(x=5, y=7)
        self.entryclient_phone.config(width=30)
        self.entryclient_phone.place(x=5, y=33)
        #Marco tabla
        self.marco_tabla.configure(width=1280, height=350)
        self.marco_tabla.place(x=110, y=480)
        self.buttonSave_client.place(x=30, y=18)
        self.buttonEdit_client.place(x=200, y=18)
        self.buttonDelete_client.place(x=350, y=18)
        self.buttonClean.place(x=520, y=18)
        self.lblsearch_clients.configure(font=("Roboto", 16))
        self.lblsearch_clients.place(x=960, y=23)
        self.entrysearch_clients.place(x=1020, y=26)
        self.tablaClientes.place_forget()
        self.tablaClientes.place(x=30, y=80)
        self.scroll.place(x=1212, y=80)
        self.tablaClientes.column("#0", width=60)
        self.tablaClientes.column("#1", width=145)
        self.tablaClientes.column("#2", width=145)
        self.tablaClientes.column("#3", width=145)
        self.tablaClientes.column("#4", width=145)
        self.tablaClientes.column("#5", width=270)
        self.tablaClientes.column("#6", width=270)
        self.tablaClientes.update()
    def on_resize(self, event):
        width_screen, height_screen = self.check_size(event)
        if width_screen >= 1440 and height_screen >= 900:
        #· Ajusta el tamaño del marco principal al 90% del ancho y alto de la ventana
            new_width = width_screen * 0.9
            new_height = height_screen * 0.9
            # Coloca e l marco principal en las coordenadas calculadas para centrarlo
            self.marco_principal.configure(width=new_width, height=new_height)
            self.marco_principal.place(relx=0.5, rely=0.5)
            
            #Reubicacion de los marcos:
            #Marco firstname
            self.marco_firstname.configure(width=235, height=65)
            self.marco_firstname.place(x=110, y=50)
            self.lblclient_firstname.configure(font=("Roboto", 15))
            self.lblclient_firstname.place(x=5, y=7)
            self.entryclient_firstname.config(width=30)
            self.entryclient_firstname.place(x=5, y=33)

            #Marco lastname
            self.marco_lastname.configure(width=235, height=65)
            self.marco_lastname.place(x=465, y=50)
            self.lblclient_lastname.configure(font=("Roboto", 15))
            self.lblclient_lastname.place(x=5, y=7)
            self.entryclient_lastname.config(width=30)
            self.entryclient_lastname.place(x=5, y=33)

            #Marco cedula
            self.marco_cedula.configure(width=235, height=65)
            self.marco_cedula.place(x=110, y=150)
            self.lblclient_ci.configure(font=("Roboto", 15))
            self.lblclient_ci.place(x=5, y=7)
            self.entryclient_ci.config(width=30)
            self.entryclient_ci.place(x=5, y=33)

            #Marco mail 
            self.marco_mail.configure(width=235, height=65)
            self.marco_mail.place(x=465, y=150)
            self.lblclient_mail.configure(font=("Roboto", 15))
            self.lblclient_mail.place(x=5, y=7)
            self.entryclient_mail.config(width=30)
            self.entryclient_mail.place(x=5, y=33)

            #Marco address
            self.marco_address.configure(width=235, height=65)
            self.marco_address.place(x=465, y=255)
            self.lblclient_address.configure(font=("Roboto", 15))
            self.lblclient_address.place(x=5, y=7)
            self.entryclient_address.config(width=30)
            self.entryclient_address.place(x=5, y=33)

            #Marco phone
            self.marco_phone.configure(width=235, height=65)
            self.marco_phone.place(x=110, y=255)
            self.lblclient_phone.configure(font=("Roboto", 15))
            self.lblclient_phone.place(x=5, y=7)
            self.entryclient_phone.config(width=30)
            self.entryclient_phone.place(x=5, y=33)

            #Marco tabla
            self.marco_tabla.configure(width=1280, height=350)
            self.marco_tabla.place(x=110, y=480)
            self.buttonSave_client.place(x=30, y=18)
            self.buttonEdit_client.place(x=200, y=18)
            self.buttonDelete_client.place(x=350, y=18)
            self.buttonClean.place(x=520, y=18)
            self.lblsearch_clients.configure(font=("Roboto", 16))
            self.lblsearch_clients.place(x=960, y=23)
            self.entrysearch_clients.place(x=1020, y=26)
            self.tablaClientes.place_forget()
            self.tablaClientes.place(x=30, y=80)
            self.scroll.place(x=1212, y=80)
            self.tablaClientes.column("#0", width=60)
            self.tablaClientes.column("#1", width=145)
            self.tablaClientes.column("#2", width=145)
            self.tablaClientes.column("#3", width=145)
            self.tablaClientes.column("#4", width=145)
            self.tablaClientes.column("#5", width=270)
            self.tablaClientes.column("#6", width=270)
            self.tablaClientes.update()

        elif width_screen <= 1440 and height_screen <= 900:
        #Retaura el tamaño original y la posición centrada del marco principal
            self.marco_principal.place(relx=0.5, rely=0.5, anchor='center')
            self.marco_principal.configure(width=self.original_width, height=self.original_height)
            #Restaurar marcos
            self.marco_firstname.configure(width=225, height=55)
            self.marco_firstname.place(x=50, y=50)
            self.lblclient_firstname.configure(font=("Roboto", 14))
            self.lblclient_firstname.place(x=5, y=1)
            self.entryclient_firstname.config(width=30)
            self.entryclient_firstname.place(x=5, y=25)
            self.marco_lastname.configure(width=225, height=55)
            self.marco_lastname.place(x=405, y=50)
            self.lblclient_lastname.configure(font=("Roboto", 14))
            self.lblclient_lastname.place(x=5,y=1)
            self.entryclient_lastname.config(width=30)
            self.entryclient_lastname.place(x=5, y=25)
            self.marco_cedula.configure(width=225, height=55)
            self.marco_cedula.place(x=50, y=150)
            self.lblclient_ci.configure(font=("Roboto", 14))
            self.lblclient_ci.place(x=5, y=1)
            self.entryclient_ci.config(width=30)
            self.entryclient_ci.place(x=5, y=25)
            self.marco_mail.configure(width=225, height=55)
            self.marco_mail.place(x=405, y=150)
            self.lblclient_mail.configure(font=("Roboto", 14))
            self.lblclient_mail.place(x=5, y=1)
            self.entryclient_mail.config(width=30)
            self.entryclient_mail.place(x=5, y=25)
            self.marco_address.configure(width=225, height=55)
            self.marco_address.place(x=405, y=255)
            self.lblclient_address.configure(font=("Roboto", 14))
            self.lblclient_address.place(x=5, y=1)
            self.entryclient_address.config(width=30)
            self.entryclient_address.place(x=5, y=25)
            self.marco_phone.configure(width=225, height=55)
            self.marco_phone.place(x=50, y=255)
            self.lblclient_phone.configure(font=("Roboto", 14))
            self.lblclient_phone.place(x=5, y=1)
            self.entryclient_phone.config(width=30)
            self.entryclient_phone.place(x=5, y=25)
            self.marco_tabla.configure(width=1080, height=300)
            self.marco_tabla.place(x=22, y=480)
            self.buttonSave_client.place(x=15, y=10)
            self.buttonEdit_client.place(x=190, y=10)
            self.buttonDelete_client.place(x=345, y=10)
            self.buttonClean.place(x=520, y=10)
            self.lblsearch_clients.configure(font=("Roboto", 14))
            self.lblsearch_clients.place(x=810, y=17)
            self.entrysearch_clients.place(x=870, y=20)
            self.tablaClientes.place_forget()
            self.tablaClientes.place(x=10, y=60)
            self.scroll.place(x=1057, y=60)
            self.tablaClientes.column("#0", width=45)
            self.tablaClientes.column("#1", width=125)
            self.tablaClientes.column("#2", width=125)
            self.tablaClientes.column("#3", width=125)
            self.tablaClientes.column("#4", width=125)
            self.tablaClientes.column("#5", width=250)
            self.tablaClientes.column("#6", width=250)
            self.tablaClientes.update()
            

    def check_size(self, event):
        width_screen = event.width
        height_screen = event.height
    
        return width_screen, height_screen
    
    def call_check_size(self, event):
        width_screen = self.winfo_width()
        height_screen = self.winfo_height()
    
        return width_screen, height_screen
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

    def ajustar_imagen(self, event):
        # Obtener el tamaño actual del label
        width = self.label_fondo.winfo_width()
        height = self.label_fondo.winfo_height()

        # Redimensionar la imagen de fondo para que se ajuste al tamaño del label
        imagen_redimensionada = self.label_fondo.resize((width, height), Image.BILINEAR)

        # Crear una instancia de PhotoImage para poder establecerla como imagen del label
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

        # Actualizar la imagen de fondo del label
        self.label_fondo.configure(image=imagen_tk)
        self.label_fondo.image = imagen_tk
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
            error_advice()

    def Depurador(self):
        self.svclient_firstname.set('')
        self.svclient_lastname.set('')
        self.svclient_ci.set('')
        self.svclient_phone.set('')
        self.svclient_address.set('')
        self.svclient_mail.set('')
        