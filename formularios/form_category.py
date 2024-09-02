import tkinter as tk
from config import  COLOR_FONDO
import PIL
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from util.util_alerts import set_opacity, save_advice, error_advice, edit_advice, delete_advice
from util.util_functions import buscarCorrelativo, actualizarCorrelativo
from functions.AdjustDepotsDao import Deposito, Grupo, AsignarDeposito, SaveGroup, EditGroup, InformacionDeposito, ListarDepositos, InformacionGrupos, ListarGrupos, obtener_depositos, obtener_grupos, obtener_CatArt, SaveDepot, EditDepot, DepotDisable
from config import COLOR_MENU_LATERAL
import datetime
from tkinter import messagebox


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

        self.marco_adjustdepot = customtkinter.CTkFrame(cuerpo_principal, width=1120, height=800, bg_color="white", fg_color="white")
        self.marco_adjustdepot.place(relx=0.5, rely=0.5, anchor="center")

        set_opacity(self.marco_adjustdepot, 0.8)
        
        self.treeviewDepositos= ttk.Treeview(self.marco_adjustdepot, height=36)
        self.treeviewDepositos.place(x=25, y=30)
        self.treeviewDepositos.heading("#0", text="Depositos Disponibles")

        self.listar_dgs()
        self.buttonCreateDepot = tk.Button(self.marco_adjustdepot, text="Crear\n Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_deposito(permisos))
        self.buttonCreateDepot.place(x=260, y=60)

        self.buttonEditDepot = tk.Button(self.marco_adjustdepot, text="Editar\n Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_deposito(permisos))
        self.buttonEditDepot.place(x=375, y=60)

        self.buttonDisableDepot = tk.Button(self.marco_adjustdepot, text="Desactivar\n Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.desactivarDeposito(permisos))
        self.buttonDisableDepot.place(x=490, y=60)

        where = ""
        if len(where) > 0:
            self.ListaDeposito = InformacionDeposito(where)
        else:
            self.ListaDeposito = ListarDepositos()
            self.ListaDeposito.reverse()
        self.tablaDeposito = ttk.Treeview(self.marco_adjustdepot, column=('codDep','name_dep','date_create','date_update'), height=15)
        self.tablaDeposito.place(x=260, y=120, height=50)

        self.tablaDeposito.heading('#0',text="ID")
        self.tablaDeposito.heading('#1',text="Cod Deposito")
        self.tablaDeposito.heading('#2',text="Nombre Deposito")
        self.tablaDeposito.heading('#3',text="DateCreated")
        self.tablaDeposito.heading('#4',text="DateUpdate")

        self.tablaDeposito.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaDeposito.column("#1", width=120, stretch=False)
        self.tablaDeposito.column("#2", width=150, stretch=False)
        self.tablaDeposito.column("#3", width=120, stretch=False)
        self.tablaDeposito.column("#4", width=120, stretch=False)

        self.treeviewDepositos.bind("<<TreeviewSelect>>", self.TEST)
        
        #INIO DE TABLA SECCION PARA GRUPOS
        self.buttonCreateGrupo = tk.Button(self.marco_adjustdepot, text="Crear\n Grupo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.crear_grupo(permisos))
        self.buttonCreateGrupo.place(x=260, y=220)

        self.buttonEditGrupo = tk.Button(self.marco_adjustdepot, text="Editar\n Grupo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.editar_deposito(permisos))
        self.buttonEditGrupo.place(x=375, y=220)

        self.buttonDisableGrupo = tk.Button(self.marco_adjustdepot, text="Desactivar\n Grupo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, 
                                        command=lambda: self.desactivarDeposito(permisos))
        self.buttonDisableGrupo.place(x=490, y=220)

        where = ""
        if len(where) > 0:
            self.ListaGrupo = InformacionGrupos(where)
        else:
            self.ListaGrupo = ListarGrupos()
            self.ListaGrupo.reverse()

        self.tablaGrupo = ttk.Treeview(self.marco_adjustdepot, column=('codgrupo','codDep','name_grupo','date_create','date_update'), height=15)
        self.tablaGrupo.place(x=260, y=280, height=100)

        self.scroll = ttk.Scrollbar(self.marco_adjustdepot, orient='vertical', command=self.tablaGrupo.yview)
        self.scroll.place(x=842, y=280, height=100)

        self.tablaGrupo.configure(yscrollcommand=self.scroll.set)
        self.tablaGrupo.tag_configure('evenrow')

        self.tablaGrupo.heading('#0',text="ID")
        self.tablaGrupo.heading('#1',text="Cod Grupo")
        self.tablaGrupo.heading('#2',text="Cod Deposito")
        self.tablaGrupo.heading('#3',text="Nombre Deposito")
        self.tablaGrupo.heading('#4',text="DateCreated")
        self.tablaGrupo.heading('#5',text="DateUpdate")

        self.tablaGrupo.column("#0", width=60, stretch=False, anchor='w')#HAY QUE CENTRARLO
        self.tablaGrupo.column("#1", width=80, stretch=False)
        self.tablaGrupo.column("#2", width=80, stretch=False)
        self.tablaGrupo.column("#3", width=120, stretch=False)
        self.tablaGrupo.column("#4", width=120, stretch=False)
        self.tablaGrupo.column("#5", width=120, stretch=False)

    def TEST(self, event):
        selected_item = self.treeviewDepositos.focus()  # Obtiene el elemento seleccionado en el Treeview
        values = self.treeviewDepositos.item(selected_item)["values"]  # Obtiene los valores del elemento seleccionado

        if len(values) > 0:  # Verifica si se seleccionó un depósito (se espera que tenga valores)
            deposito_id = values[0]
            deposito_name = values[1]  # Obtiene el valor del depósito seleccionado

            # Llama a la función InformacionDeposito con el depósito seleccionado como parámetro
            deposito_info = InformacionDeposito(f"WHERE codDep = {deposito_id} AND name_dep = '{deposito_name}'")

            self.tablaDeposito.delete(*self.tablaDeposito.get_children())
            self.tablaGrupo.delete(*self.tablaGrupo.get_children())

            if deposito_info: 
                self.tablaDeposito.insert('', 0, text=deposito_info[0][0], values=(deposito_info[0][1], 
                                        deposito_info[0][2], deposito_info[0][3], deposito_info[0][4]))  # Inserta la información del depósito en la tabla

                codDep = deposito_info[0][1]
                grupos = InformacionGrupos(f"WHERE codDep = {codDep}")

                for grupo in grupos:
                    self.tablaGrupo.insert('', 'end', text=grupo[0], values=(grupo[1], grupo[2], grupo[3], grupo[4], grupo[5]))


    def SincronizarInformacionDepositos(self, event):
            self.selected_item = self.treeviewDepositos.focus()  # Obtiene el elemento seleccionado en el Treeview
            self.deposito_id = self.treeviewDepositos.item(self.selected_item)["values"][0]  # Obtiene el valor del depósito seleccionado

            # Llama a la función InformacionDeposito con el depósito seleccionado como parámetro
            self.deposito_info = InformacionDeposito(f"WHERE codDep = {self.deposito_id}")

            self.tablaDeposito.delete(*self.tablaDeposito.get_children())

            if self.deposito_info:  # Borra el contenido actual de la tabla
                self.tablaDeposito.insert('', 0, text=self.deposito_info[0][0], values=(self.deposito_info[0][1], self.deposito_info[0][2], self.deposito_info[0][3], self.deposito_info[0][4], self.deposito_info[0][5]))  # Inserta la información del depósito en la tabla
            
                codDep = self.deposito_info[0][1]

                self.SincronizarGrupos(codDep)

    def SincronizarGrupos(self, codDep):

        self.tablaGrupo.delete(*self.tablaGrupo.get_children())
        # Obtiene los grupos relacionados con el código del depósito
        grupos = InformacionGrupos(f"WHERE codDep = {codDep}")  # Reemplaza "ObtenerGruposPorDeposito" con la función o método adecuado para obtener los grupos relacionados con el código del depósito
        # Inserta los grupos en la tabla
        for grupo in grupos:
            self.tablaGrupo.insert('', 'end', text=grupo[0], values=(grupo[1], grupo[2], grupo[3], grupo[4], grupo[5]))

    def crear_deposito(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateDepot = customtkinter.CTkToplevel()
        self.topCreateDepot.title("Crear Deposito")
        self.topCreateDepot.w = 400
        self.topCreateDepot.h = 250
        self.topCreateDepot.geometry(f"{self.topCreateDepot.w}x{self.topCreateDepot.h}")
        self.topCreateDepot.resizable(False, False)
        self.topCreateDepot.configure(bg_color='#6a717e')
        self.topCreateDepot.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topCreateDepot.winfo_screenwidth()
        screen_height = self.topCreateDepot.winfo_screenheight()
        x = (screen_width - self.topCreateDepot.w) // 2
        y = (screen_height - self.topCreateDepot.h) // 2
        self.topCreateDepot.geometry(f"+{x}+{y}")

        self.topCreateDepot.lift()
        self.topCreateDepot.grab_set()
        self.topCreateDepot.transient()

        marco_createDepot = customtkinter.CTkFrame(self.topCreateDepot, width=350,height=200, bg_color="white", fg_color="white")
        marco_createDepot.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_createDepot, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_createDepot, text="Crear Deposito", font=("Roboto",13))
        self.lblinfo.place(x=133, rely=0.1)

        self.lblnombre_deposito = customtkinter.CTkLabel(marco_createDepot, text='Nombre del Deposito', font=("Roboto", 13))
        self.lblnombre_deposito.place(x=120, y=60)

        self.svnombre_deposito = customtkinter.StringVar()
        self.entrynombre_deposito = ttk.Entry(marco_createDepot, style='Modern.TEntry', textvariable=self.svnombre_deposito)
        self.entrynombre_deposito.place(x=120, y=90)
        self.entrynombre_deposito.configure(style='Entry.TEntry')

        self.buttonCrearDeposito = tk.Button(marco_createDepot, text="Crear Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarDeposito)
        self.buttonCrearDeposito.place(x=118, y=140)

    def crear_grupo(self, permisos):
        self.id = None
        #Creacion del top level
        self.topCreateGroup = customtkinter.CTkToplevel()
        self.topCreateGroup.title("Crear Grupo")
        self.topCreateGroup.w = 550
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
        marco_createGroup.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_createGroup, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_createGroup, text="Crear Grupo para un Deposito ", font=("Roboto",13))
        self.lblinfo.place(x=140, rely=0.1)

        depositos = AsignarDeposito()
        self.svdepositoAsig = customtkinter.StringVar(value="Selecciona un Deposito")
        self.multioption = customtkinter.CTkOptionMenu(marco_createGroup, values=[deposito[2] for deposito in depositos], variable=self.svdepositoAsig)
        self.multioption.place(x=40, y=87)

        self.lblnombre_grupo = customtkinter.CTkLabel(marco_createGroup, text='Nombre del Grupo', font=("Roboto", 13))
        self.lblnombre_grupo.place(x=245, y=60)

        self.svnombre_grupo = customtkinter.StringVar()
        self.entrynombre_grupo = ttk.Entry(marco_createGroup, style='Modern.TEntry', textvariable=self.svnombre_grupo)
        self.entrynombre_grupo.place(x=245, y=92)
        self.entrynombre_grupo.configure(style='Entry.TEntry')

        self.buttonCrearGrupo = tk.Button(marco_createGroup, text="Crear Grupo", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarGrupo)
        self.buttonCrearGrupo.place(x=155, y=190)

    def editar_deposito(self, permisos):
        selected_item = self.treeviewDepositos.selection()
        if selected_item:
            item_values = self.treeviewDepositos.item(selected_item)
            self.id = item_values['values'][0]
            self.nombre_deposito = item_values['text']
        #Creacion del top level
        self.topEditDepot = customtkinter.CTkToplevel()
        self.topEditDepot.title("Crear Modulo")
        self.topEditDepot.w = 400
        self.topEditDepot.h = 250
        self.topEditDepot.geometry(f"{self.topEditDepot.w}x{self.topEditDepot.h}")
        self.topEditDepot.resizable(False, False)
        self.topEditDepot.configure(bg_color='#6a717e')
        self.topEditDepot.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topEditDepot.winfo_screenwidth()
        screen_height = self.topEditDepot.winfo_screenheight()
        x = (screen_width - self.topEditDepot.w) // 2
        y = (screen_height - self.topEditDepot.h) // 2
        self.topEditDepot.geometry(f"+{x}+{y}")

        self.topEditDepot.lift()
        self.topEditDepot.grab_set()
        self.topEditDepot.transient()

        marco_EditDepot = customtkinter.CTkFrame(self.topEditDepot, width=350,height=200, bg_color="white", fg_color="white")
        marco_EditDepot.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_EditDepot, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_EditDepot, text="Editar Deposito", font=("Roboto",13))
        self.lblinfo.place(x=133, rely=0.1)

        self.lblnombre_deposito = customtkinter.CTkLabel(marco_EditDepot, text='Nombre del Deposito', font=("Roboto", 13))
        self.lblnombre_deposito.place(x=120, y=60)

        self.svnombre_deposito = customtkinter.StringVar(value=self.nombre_deposito)
        self.entrynombre_deposito = ttk.Entry(marco_EditDepot, style='Modern.TEntry', textvariable=self.svnombre_deposito)
        self.entrynombre_deposito.place(x=120, y=90)
        self.entrynombre_deposito.configure(style='Entry.TEntry')

        self.buttonEditarDeposito = tk.Button(marco_EditDepot, text="Editar Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarDeposito)
        self.buttonEditarDeposito.place(x=118, y=140)

    def editar_grupo(self, permisos):
        selected_item = self.treeviewDepositos.selection()
        if selected_item:
            item_values = self.treeviewDepositos.item(selected_item)
            self.id = item_values['values'][0]
            self.nombre_deposito = item_values['text']
        #Creacion del top level
        self.topEditDepot = customtkinter.CTkToplevel()
        self.topEditDepot.title("Crear Modulo")
        self.topEditDepot.w = 400
        self.topEditDepot.h = 250
        self.topEditDepot.geometry(f"{self.topEditDepot.w}x{self.topEditDepot.h}")
        self.topEditDepot.resizable(False, False)
        self.topEditDepot.configure(bg_color='#6a717e')
        self.topEditDepot.configure(fg_color='#6a717e')
        
        #Centrar la ventana en la pantalla
        screen_width = self.topEditDepot.winfo_screenwidth()
        screen_height = self.topEditDepot.winfo_screenheight()
        x = (screen_width - self.topEditDepot.w) // 2
        y = (screen_height - self.topEditDepot.h) // 2
        self.topEditDepot.geometry(f"+{x}+{y}")

        self.topEditDepot.lift()
        self.topEditDepot.grab_set()
        self.topEditDepot.transient()

        marco_EditDepot = customtkinter.CTkFrame(self.topEditDepot, width=350,height=200, bg_color="white", fg_color="white")
        marco_EditDepot.place(relx=0.5, rely=0.5, anchor="center")
        
        set_opacity(marco_EditDepot, 0.8)

        self.lblinfo = customtkinter.CTkLabel(marco_EditDepot, text="Editar Deposito", font=("Roboto",13))
        self.lblinfo.place(x=133, rely=0.1)

        self.lblnombre_deposito = customtkinter.CTkLabel(marco_EditDepot, text='Nombre del Deposito', font=("Roboto", 13))
        self.lblnombre_deposito.place(x=120, y=60)

        self.svnombre_deposito = customtkinter.StringVar(value=self.nombre_deposito)
        self.entrynombre_deposito = ttk.Entry(marco_EditDepot, style='Modern.TEntry', textvariable=self.svnombre_deposito)
        self.entrynombre_deposito.place(x=120, y=90)
        self.entrynombre_deposito.configure(style='Entry.TEntry')

        self.buttonEditarDeposito = tk.Button(marco_EditDepot, text="Editar Deposito", font=("Roboto", 12), bg=COLOR_MENU_LATERAL, bd=0,fg="white", anchor="w", compound=tk.LEFT, padx=10, command=self.GuardarDeposito)
        self.buttonEditarDeposito.place(x=118, y=140)

    def desactivarDeposito(self, permisos):
        try:
            self.id = self.treeviewDepositos.item(self.treeviewDepositos.selection())['values'][0]
            confirmar = messagebox.askyesno("Confirmar", "¿Estas seguro de que deseas desactivar este deposito?")

            if confirmar:
                DepotDisable(self.id)
                self.listar_dgs()

        except Exception as e:
            error_advice()
            mensaje = f'Error en desactivarDeposito, form_adjustdepot: {str(e)}'
            with open('error_log.txt', 'a') as file:
                file.write(mensaje + '\n')

    def listar_dgs(self):
        self.treeviewDepositos.delete(*self.treeviewDepositos.get_children())
        depositos = obtener_depositos()
    
        for deposito in depositos:
            deposito_id = deposito[0]
            deposito_codDep = deposito[1]
            deposito_name = deposito[2]

            deposito_item = self.treeviewDepositos.insert("", "end", text=deposito_name, values=(deposito_codDep,deposito_name), tags=("Deposito", deposito_codDep, deposito_name))

            groups = obtener_grupos(deposito_codDep)

            for group in groups:
                group_id = group[0]
                group_codgrupo = group[1]
                group_codDep = group[2]
                group_name = group[3]

                group_item = self.treeviewDepositos.insert(deposito_item, "end", text=group_name, values=(group_codDep, group_name), tags=("group", group_codDep, group_name))

                subgroups = obtener_CatArt(group_codgrupo)

                for subgroup in subgroups:
                    subgroup_id = subgroup[0]
                    subgroup_codgrupo = subgroup[2]
                    subgroup_name = subgroup[3]

                    self.treeviewDepositos.insert(group_item, "end", text=subgroup_name, values=(subgroup[0],), tags=("subgroup", subgroup[0]))

    def GuardarDeposito(self):
        codDep = buscarCorrelativo('deposito')
        codDep = codDep + 1

        fecha_actual = datetime.datetime.now()
        date_created = fecha_actual.strftime("%d/%m/%Y")
        date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
        
        deposito = Deposito(
            codDep,
            self.svnombre_deposito.get(),
            date_created,
            date_update
        )
        if self.id is None:
            SaveDepot(deposito)
            actualizarCorrelativo('deposito')
            self.topCreateDepot.destroy()
        else:
            EditDepot(deposito, self.id)
            self.topEditDepot.destroy()
        self.listar_dgs()
        

    def GuardarGrupo(self):
        codGrupo = buscarCorrelativo('grupo')
        codGrupo = codGrupo + 1

        fecha_actual = datetime.datetime.now()
        date_created = fecha_actual.strftime("%d/%m/%Y")
        date_update = fecha_actual.strftime("%d/%m/%y %H:%M:%S")
        depositoAsignado = self.svdepositoAsig.get()
        codDep = None
        for deposito in AsignarDeposito():
                if deposito[2] == depositoAsignado:
                    codDep = deposito[1]
                    break
        grupo = Grupo(
            codGrupo,
            codDep,
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
        self.listar_dgs()
        