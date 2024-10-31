import tkinter as tk
from config import  COLOR_FONDO
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.old_functions import buscarCorrelativo, actualizarCorrelativo
from util.util_screen import loadBackgroundImage, centerWidget, set_window_icon
from functions.DepotsDao import deposit, searchDepots, listDepot, getDepots,  save_depot, edit_depot, depotDisable, listInactiveDepot, recoverDepot
from config import COLOR_MENU_LATERAL
import datetime
from tkinter import messagebox


class FormDepot():

    def __init__(self, cuerpo_principal, permisos):
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(cuerpo_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.cuerpo_principal = tk.Frame(cuerpo_principal)
        self.cuerpo_principal.pack(side=tk.BOTTOM, fill='both', expand=True)  

        loadBackgroundImage(self)

        self.frame_depot = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.frame_depot.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.frame_depot, 0.94)
        
        ### Nuevo modelo para botones:
        self.buttonNewDepot = customtkinter.CTkButton(self.frame_depot, text="Nuevo\nDepósito", width=80, height=60, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.FormNewDepot(permisos))
        self.buttonNewDepot.place(x=180, y=60)

        if 'ALMA1008' in permisos:
            self.buttonEditDepot = customtkinter.CTkButton(self.frame_depot,  text="Editar\nDepósito", width=80, height=60, state='normal', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.depotsTable.item(self.depotsTable.selection())['values']))
            self.buttonEditDepot.place(x=290, y=60)
        else: 
            self.buttonEditDepot = customtkinter.CTkButton(self.frame_depot,  text="Editar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.depotsTable.item(self.depotsTable.selection())['values']))
            self.buttonEditDepot.place(x=290, y=60)
            
        if 'ALMA1008' in permisos:
           self.buttonDisableDepot = customtkinter.CTkButton(self.frame_depot,  text="Desactivar\nDepósito", width=80, height=60, state='normal', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
           self.buttonDisableDepot.place(x=400, y=60)
        else:
            self.buttonDisableDepot = customtkinter.CTkButton(self.frame_depot,  text="Desactivar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableDepot.place(x=400, y=60)

        #Switch de activos/inactivos
        if 'ALMA1010' in permisos:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchStatus = customtkinter.CTkSwitch(self.frame_depot, variable=self.switchStatus, state='normal', text="Activos", font=("Roboto", 12), command=lambda: self.showStatus(permisos))
            self.switchStatus.place(x=800, y=130)
        else:
            self.switchStatus = tk.BooleanVar(value=True)
            self.switchStatus = customtkinter.CTkSwitch(self.frame_depot, variable=self.switchStatus, state='disabled', text="Activos", font=("Roboto", 12), command=lambda: self.showStatus(permisos))
            self.switchStatus.place(x=800, y=130)
        ################## Informacion de la tabla #############
        where = ""
        if len(where) > 0:
            self.depositList = searchDepots(where)
        else:
            self.depositList = listDepot()
            self.depositList.reverse()

        self.depotsTable = ttk.Treeview(self.frame_depot, column=('codDep','name_dep','date_create','updated_at'), height=18)
        self.depotsTable.place(x=180, y=165)

        self.depotsTable.heading('#0',text="ID")
        self.depotsTable.heading('#1',text="CodDeposito")
        self.depotsTable.heading('#2',text="NombreDeposito")
        self.depotsTable.heading('#3',text="Created_at")
        self.depotsTable.heading('#4',text="Updated_at")

        self.depotsTable.column("#0", width=100, stretch=False)
        self.depotsTable.column("#1", width=100, stretch=False)
        self.depotsTable.column("#2", width=200, stretch=False)
        self.depotsTable.column("#3", width=150, stretch=False)
        self.depotsTable.column("#4", width=150, stretch=False)

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
        for col in ('#0', '#1', '#2', '#3', '#4'):
            self.depotsTable.heading(col, command=lambda _col=col: sort_column(self.depotsTable, _col, False))

        # Alternancia de colores en las filas
        self.depotsTable.tag_configure('odd', background='#E8E8E8')   # Estilo para filas impares
        self.depotsTable.tag_configure('even', background='#DFDFDF')  # Estilo para filas pares

        for i, p in enumerate(self.depositList):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.depotsTable.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4]), tags=(tag,))
        
        self.depotsTable.bind('<Double-1>', lambda event: self.FormEditDepot(event, self.depotsTable.item(self.depotsTable.selection())['values']))

    def showStatus(self, permisos):
        if self.switchStatus.get() == True:
            self.switchStatus.configure(text="Activos")
            self.showActive(permisos)
        else:
            self.switchStatus.configure(text="Inactivos")
            self.showInactive(permisos)
     
    def showActive(self, permisos):
        self.buttonNewDepot = customtkinter.CTkButton(self.frame_depot, text="Nuevo\nDepósito", width=80, height=60, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.FormNewDepot(permisos))
        self.buttonNewDepot.place(x=180, y=60)
        if 'ALMA1008' in permisos:
            self.buttonEditDepot = customtkinter.CTkButton(self.frame_depot,  text="Editar\nDepósito", width=80, height=60, state='normal', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.depotsTable.item(self.depotsTable.selection())['values']))
            self.buttonEditDepot.place(x=290, y=60)
        else: 
            self.buttonEditDepot = customtkinter.CTkButton(self.frame_depot,  text="Editar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.depotsTable.item(self.depotsTable.selection())['values']))
            self.buttonEditDepot.place(x=290, y=60)
        if 'ALMA1010' in permisos:
            self.buttonDisableDepot = customtkinter.CTkButton(self.frame_depot,  text="Desactivar\nDepósito", width=80, height=60, state='enabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableDepot.place(x=400, y=60)
        else:
            self.buttonDisableDepot = customtkinter.CTkButton(self.frame_depot,  text="Desactivar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableDepot.place(x=400, y=60)
        # Borrar los elementos existentes en la tabla de permisos
        self.depotsTable.delete(*self.depotsTable.get_children())
        
        # Obtener la lista de permisos activos
        active_depots = listDepot()
        # Insertar los permisos activos en la tabla
        for i, p in enumerate(active_depots):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.depotsTable.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4]), tags=(tag,))

    def showInactive(self, permisos):
        if 'ALMA1011' in permisos:
            self.buttonNewDepot = customtkinter.CTkButton(self.frame_depot, text="Restaurar\nDepósito", width=80, height=60, state='normal',font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.restoreDepot(permisos))
            self.buttonNewDepot.place(x=180, y=60)
        else:
            self.buttonNewDepot = customtkinter.CTkButton(self.frame_depot, text="Restaurar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.restoreDepot(permisos))
            self.buttonNewDepot.place(x=180, y=60)
        if 'ALMA1008' in permisos:
            self.buttonEditDepot = customtkinter.CTkButton(self.frame_depot,  text="Editar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.depotsTable.item(self.depotsTable.selection())['values']))
            self.buttonEditDepot.place(x=290, y=60)
        else: 
            self.buttonEditDepot = customtkinter.CTkButton(self.frame_depot,  text="Editar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.FormEditDepot(permisos, self.depotsTable.item(self.depotsTable.selection())['values']))
            self.buttonEditDepot.place(x=290, y=60)
        if 'ALMA1010' in permisos:
            self.buttonDisableDepot = customtkinter.CTkButton(self.frame_depot,  text="Desactivar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableDepot.place(x=400, y=60)
        else:
            self.buttonDisableDepot = customtkinter.CTkButton(self.frame_depot,  text="Desactivar\nDepósito", width=80, height=60, state='disabled', font=("Roboto", 15),  fg_color="#2C3E50",  hover_color="#34495E",  text_color="white",  corner_radius=7, command=lambda: self.inactivateDepot(permisos))
            self.buttonDisableDepot.place(x=400, y=60)
            
        self.depotsTable.delete(*self.depotsTable.get_children())
        self.depotsTable.heading('#4', text='Deleted_at')
        inactive_depots = listInactiveDepot()
        for i, p in enumerate(inactive_depots):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.depotsTable.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[5]), tags=(tag,))


    def FormNewDepot(self, permisos):
        self.id = None
        #Creacion del top level
        self.topNewDepot = tk.Toplevel()
        self.topNewDepot.title("Crear Deposito")
        self.topNewDepot.w = 400
        self.topNewDepot.h = 250
        self.topNewDepot.geometry(f"{self.topNewDepot.w}x{self.topNewDepot.h}")
        self.topNewDepot.resizable(False, False)
        set_window_icon(self.topNewDepot)
        centerWidget(self.topNewDepot)
        
        self.topNewDepot.config(bg='#6a717e')
        #self.topNewDepot.config(fg='#6a717e')
        self.topNewDepot.lift()
        self.topNewDepot.grab_set()
        self.topNewDepot.transient()

        frame_createDepot = customtkinter.CTkFrame(self.topNewDepot, width=350,height=200, bg_color="white", fg_color="white")
        frame_createDepot.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(frame_createDepot, 0.8)      
        self.lblnombre_deposito = customtkinter.CTkLabel(frame_createDepot, text='Nombre del Deposito', font=("Roboto", 15))        
        self.lblnombre_deposito.place(x=110, y=25)        
        # Actualización del Entry
        style = ttk.Style()
        style.configure(
            'Modern.TEntry',
            background="#2C3E50",  # Fondo oscuro similar al botón
            #foreground="black",     # Texto en blanco
            fieldbackground="#34495E",  # Color de fondo cuando el entry es editable
            bordercolor="#34495E",
            padding=[5, 8]
        )
        self.svnombre_deposito = customtkinter.StringVar()
        self.entrynombre_deposito = ttk.Entry(frame_createDepot, 
                                            style='Modern.TEntry', 
                                            textvariable=self.svnombre_deposito, 
                                            font=("Roboto", 13),
                                            justify='center')
        self.entrynombre_deposito.place(x=70, y=70)
        
        self.buttonCrearDeposito = customtkinter.CTkButton(frame_createDepot, text="Nuevo\nDepósito", width=70, height=50, font=("Roboto", 15), fg_color="#2C3E50", hover_color="#34495E", text_color="white", corner_radius=7, command=lambda: self.SaveDepot)
        self.buttonCrearDeposito.place(x=135, y=135)
        
    def FormEditDepot(self, permisos, values):
        if values:
            # Obtener el id y nombre del depósito seleccionado
            self.id = self.depotsTable.item(self.depotsTable.selection())['text']
            self.nombre_deposito = self.depotsTable.item(self.depotsTable.selection())['values'][1]

            # Creación del top level
            self.topEditDepot = tk.Toplevel()
            self.topEditDepot.title("Editar Deposito")
            self.topEditDepot.w = 400
            self.topEditDepot.h = 250
            self.topEditDepot.geometry(f"{self.topEditDepot.w}x{self.topEditDepot.h}")
            self.topEditDepot.resizable(False, False)
            self.topEditDepot.configure(bg='#6a717e')
            set_window_icon(self.topEditDepot)
            centerWidget(self.topEditDepot)
            self.topEditDepot.lift()
            self.topEditDepot.grab_set()
            self.topEditDepot.transient()

            # Frame para editar el depósito
            frame_editDepot = customtkinter.CTkFrame(self.topEditDepot, width=350, height=200, bg_color="white", fg_color="white")
            frame_editDepot.place(relx=0.5, rely=0.5, anchor="center")

            set_opacity(frame_editDepot, 0.8)

            # Etiqueta y entry para el nombre del depósito
            self.lblnombre_deposito = customtkinter.CTkLabel(frame_editDepot, text='Nombre del Deposito', font=("Roboto", 15))
            self.lblnombre_deposito.place(x=110, y=25)

            # Actualización del estilo del Entry
            style = ttk.Style()
            style.configure(
                'Modern.TEntry',
                background="#2C3E50",  # Fondo oscuro similar al botón
                fieldbackground="#34495E",  # Color de fondo cuando el entry es editable
                bordercolor="#34495E",
                padding=[5, 8]
            )

            # Entry para editar el nombre del depósito
            self.svnombre_deposito = customtkinter.StringVar(value=self.nombre_deposito)
            self.entrynombre_deposito = ttk.Entry(
                frame_editDepot, 
                style='Modern.TEntry', 
                textvariable=self.svnombre_deposito, 
                font=("Roboto", 13),
                justify='center')
            self.entrynombre_deposito.place(x=70, y=70)

            # Botón para editar el depósito
            self.buttonEditarDeposito = customtkinter.CTkButton(
                frame_editDepot, 
                text="Editar\nDepósito", 
                width=70, 
                height=50, 
                font=("Roboto", 15), 
                fg_color="#2C3E50", 
                hover_color="#34495E", 
                text_color="white", 
                corner_radius=7, 
                command=lambda: self.SaveDepot()
            )
            self.buttonEditarDeposito.place(x=135, y=135)
        else:
            messagebox.showerror("Error", "Debe seleccionar un depósito")

    def inactivateDepot(self, permisos):
        try:
            self.id = self.depotsTable.item(self.depotsTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas desactivar este deposito?")

            if confirmar:
                depotDisable(self.id)

            self.updateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en inactivateDepot, form_adjustdepot: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                
    def restoreDepot(self, permisos):
        try:
            self.id = self.depotsTable.item(self.depotsTable.selection())['text']
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas restaurar este deposito?")

            if confirmar:
                recoverDepot(self.id)
                self.switchStatus.select(True)
                self.showStatus(permisos)
                self.updateTable()

        except Exception as e:
            error_advice()
            mensaje = f'Error en inactivateDepot, form_adjustdepot: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')
                

    def SaveDepot(self):
        codDep = buscarCorrelativo('deposito')
        codDep = codDep + 1

        fecha_actual = datetime.datetime.now()
        created_at = fecha_actual.strftime("%Y-%m-%d")
        updated_at = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
        deleted_at = 'NULL'
        
        deposito = deposit(
            codDep,
            self.svnombre_deposito.get(),
            created_at,
            updated_at,
            deleted_at
        )
        
        if self.id is None:
            save_depot(deposito)
            actualizarCorrelativo('deposito')
            self.topNewDepot.destroy()
        else:
            edit_depot(deposito, self.id)
            self.topEditDepot.destroy()
        self.updateTable()
        
    def updateTable(self, where=None):
        try:
        # Limpiar la tabla existente
            self.depotsTable.delete(*self.depotsTable.get_children())

            if where is not None and len(where) > 0:
                self.depositList = searchDepots(where)
            else:
                self.depositList = listDepot()
                self.depositList.reverse()
            for i, p in enumerate(self.depositList):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.depotsTable.insert('',0,text=p[0], values=(p[1],p[2],p[3],p[4]), tags=(tag,))
        except Exception as e:
            error_advice()
            mensaje = f'Error en updateTable, form_depot: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')