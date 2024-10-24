import customtkinter
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class Button:
    def __init__(self, frame, text, command, x, y, state='normal'):
        self.buton = customtkinter.CTkButton(frame,
                                             text=text,
                                             state=state,
                                             width=80,
                                             height=60,
                                             font=("Roboto", 15),
                                             fg_color="#2C3E50",
                                             hover_color="#34495E",
                                             text_color="white",
                                             corner_radius=7,
                                             command=command
                                             )
        self.buton.place(x=x, y=y)

class Switch:
    def __init__(self, frame, command, x, y, text="", state='normal', variable=None):
        if variable is True:
            variable = tk.BooleanVar(value=True)
            text="Activos"
        else:
            text="Inactivos"
            variable = tk.BooleanVar(value=False)
            
        self.switch = customtkinter.CTkSwitch(frame,
                                            text=text,
                                            state=state,
                                            command=lambda: command,
                                            variable=variable,
                                            fg_color="#2C3E50",
                                            progress_color="#34495E", 
                                            button_color="#1ABC9C", 
                                            button_hover_color="#16A085")
        self.switch.place(x=x, y=y)  
        
    #def get(self):
    #    # Devuelve el estado actual del switch (True para activos, False para inactivos)
    #    return svariable.get()      

class SearchBar:
    def __init__(self, frame, icon_path, x, y, db_table, search_fields, dataList, dataTable):
        self.db_table = db_table
        self.search_fields = search_fields
        self.dataList = dataList
        self.dataTable = dataTable
        
        # Cargar y redimensionar la imagen del ícono de búsqueda
        search_image = Image.open(icon_path)
        search_resized = search_image.resize((30, 30))  # Puedes ajustar el tamaño del ícono aquí
        self.search_icon = ImageTk.PhotoImage(search_resized)

        # Crear el label con el ícono de búsqueda
        self.lblsearch = customtkinter.CTkLabel(frame, text='',
                                                image=self.search_icon, 
                                                font=("Roboto", 14))
        self.lblsearch.place(x=x, y=y)

        # Crear el campo de entrada con una variable StringVar
        self.sv_entry_search = tk.StringVar()
        self.entry_search = ttk.Entry(frame, textvariable=self.sv_entry_search, 
                                      style='Modern.TEntry', width=30)
        self.entry_search.place(x=x+35, y=y+2)
        # Asignar el comando para ejecutar al escribir en el campo de búsqueda
        self.entry_search.bind('<KeyRelease>', self.updateSearch)
        
    def get_search_text(self):
        return self.sv_entry_search.get()

    def set_search_text(self, text):
        self.sv_entry_search.set(text)
        
    def updateSearch(self, event=None):
        # Conectar a la base de datos
        connection = sqlite3.connect('database/database.db')
        cursor = connection.cursor()

        # Obtener el contenido del Entry
        content = self.sv_entry_search.get().lower()

        # Crear la consulta SQL dinámica
        query = f"SELECT * FROM {self.db_table} WHERE " + " OR ".join([f"{field} LIKE ?" for field in self.search_fields])

        # Ejecutar la consulta
        cursor.execute(query, tuple(f"%{content}%" for _ in self.search_fields))

        # Obtener los resultados de la consulta
        result = cursor.fetchall()

        # Filtrar los registros según el contenido ingresado
        filtered_results = []
        for p in self.dataList:
            if any(content.lower() in str(p[i]).lower() for i in range(len(p))):
                filtered_results.append(p)

        # Borrar los elementos existentes en la tabla
        self.dataTable.clear_table()
        # Insertar los nuevos resultados en la tabla
        for p in filtered_results:
            self.dataTable.insert_row(p)
        # Cerrar la conexión a la base de datosc
        cursor.close()
        connection.close()


class Table:
    def __init__(self, frame, headers, 
                 data_list, 
                 edit_command=None, 
                 x=32, y=200, 
                 row_height=32, 
                 table_height=25):
        self.frame = frame
        self.headers = headers
        self.data_list = data_list
        self.edit_command = edit_command

        # Crear tabla (Treeview) con columnas dinámicas
        self.table = ttk.Treeview(frame, columns=headers, height=table_height)
        self.table.place(x=x, y=y)

        # Scrollbar vertical
        self.scroll = ttk.Scrollbar(frame, orient='vertical', command=self.table.yview)
        self.scroll.place(x=x+1052, y=y, height=526)  # Ajustar posición del scrollbar
        self.table.configure(yscrollcommand=self.scroll.set)

        # Configuración de las columnas y encabezados
        self._configure_columns()

        # Configuración del estilo personalizado
        self._configure_style(row_height)

        # Llenar la tabla con los datos
        self._fill_table()

        # Asociar el evento de doble clic (si se proporciona un comando de edición)
        if edit_command:
            self.table.bind('<Double-1>', lambda event: self._on_double_click(event))

    def _configure_columns(self):
        # Definir encabezados y anchos dinámicos según los headers proporcionados
        self.table.heading('#0', text="ID")  # Columna #0 es el ID por defecto
        self.table.column("#0", width=50, stretch=True, anchor='w')

        for i, header in enumerate(self.headers):
            col_id = f'#{i+1}'
            self.table.heading(col_id, text=header)
            self.table.column(col_id, width=100, stretch=True)

    def _configure_style(self, row_height):
        # Crear estilo personalizado
        style = ttk.Style()
        style.configure("Treeview", 
                        background="white",
                        foreground="black",
                        relief="flat",
                        rowheight=row_height,  # Altura de las filas configurable
                        fieldbackground="white")
        style.map("Treeview", 
                  background=[("selected", "#347083")],  # Color de fila seleccionada
                  foreground=[("selected", "white")])    # Texto de fila seleccionada

        # Alternancia de colores en las filas
        self.table.tag_configure('odd', background='#E8E8E8')  # Fila impar
        self.table.tag_configure('even', background='#DFDFDF')  # Fila par

    def _fill_table(self):
        # Llenar la tabla con los datos proporcionados
        for i, data in enumerate(self.data_list):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.table.insert('', 'end', text=data[0], values=data[1:], tags=(tag,))

    def _on_double_click(self, event):
        # Ejecutar el comando de edición al hacer doble clic en una fila
        selected_item = self.table.item(self.table.selection())
        if selected_item['values'] and self.edit_command:
            self.edit_command(selected_item['values'])

    def sort_column(self, col, reverse):
        # Ordenar columna
        if col == '#0':
            data_list = [(self.table.item(child, 'text'), child) for child in self.table.get_children('')]
        else:
            data_list = [(self.table.set(child, col), child) for child in self.table.get_children('')]

        # Ordenar lista
        data_list.sort(reverse=reverse)

        # Reorganizar elementos en el Treeview
        for index, (val, child) in enumerate(data_list):
            self.table.move(child, '', index)

        # Actualizar encabezado para alternar ordenación en próximos clics
        self.table.heading(col, command=lambda: self.sort_column(col, not reverse))

    def enable_sorting(self):
        # Habilitar ordenación por columna
        for i, _ in enumerate(self.headers):
            col_id = f'#{i+1}'
            self.table.heading(col_id, command=lambda _col=col_id: self.sort_column(_col, False))

    def clear_table(self):
        # Eliminar todos los elementos de la tabla
        for item in self.table.get_children():
            self.table.delete(item)

    def insert_row(self, data):
        # Insertar una nueva fila en la tabla
        tag = 'even' if len(self.table.get_children()) % 2 == 0 else 'odd'
        self.table.insert('', 'end', text=data[0], values=data[1:], tags=(tag,))


  
        