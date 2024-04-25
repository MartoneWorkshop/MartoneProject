from .conexion import ConexionDB
from tkinter import messagebox

def EditClient(clients, id_client):
    conexion = ConexionDB()
    sql = f"""UPDATE Clients SET client_firstname = '{clients.client_firstname}', client_lastname = '{clients.client_lastname}', client_ci = '{clients.client_ci}', client_phone = '{clients.client_phone}', client_address = '{clients.client_address}', client_mail = '{clients.client_mail}', activo = 1 WHERE id_client = {id_client}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        title = 'Actualizar Cliente'
        mensaje = 'Los datos del cliente han sido actualizados.'
        messagebox.showinfo(title, mensaje)
    except Exception as e:
        conexion.cerrarConexion()
        title = 'Error de Sistema'
        mensaje = f'Error en Editar el cliente: {str(e)}'
        messagebox.showerror(title, mensaje)
    
def SaveClient(clients):
    conexion = ConexionDB()
    sql = f"""INSERT INTO Clients (client_firstname, client_lastname, client_ci, client_phone, client_address, client_mail, activo)
    VALUES('{clients.client_firstname}','{clients.client_lastname}','{clients.client_ci}','{clients.client_phone}','{clients.client_address}','{clients.client_mail}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        title = 'Save Client'
        mensaje = 'El cliente ha sido registrado con exito.'
        messagebox.showinfo(title, mensaje)
    except Exception as e:
        conexion.cerrarConexion()
        title = 'Error de Sistema'
        mensaje = f'Error en SaveClient: {str(e)}'
        messagebox.showerror(title, mensaje)

def listarCliente():
    conexion = ConexionDB()
    listaCliente = []
    sql = 'SELECT * FROM Clients WHERE activo = 1'
    
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        title = 'Error de Sistema'
        mensaje = f'Error en listarCliente: {str(e)}'
        messagebox.showwarning (title, mensaje)
    return listaCliente

def clientArchived():
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM Clients WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        title = 'Error de Sistema'
        mensaje = f'Error clientArchived: {str(e)}'
        messagebox.showwarning (title, mensaje)
    return listaCliente    

def consulClient(where):
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM Clients {where}'
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        title = 'Error de Sistema'
        mensaje = f'Error en consulClient: {str(e)}'
        messagebox.showwarning (title, mensaje)
    return listaCliente

def client_Delete(id_client):
    conexion = ConexionDB()
    sql = f'UPDATE Clients SET activo = 0 WHERE id_client = {id_client}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        title = 'Eliminar Cliente'
        mensaje = 'Registro de cliente eliminado exitosamente.'
        messagebox.showinfo (title, mensaje)

    except Exception as e:
        conexion.cerrarConexion()
        title = 'Error de Sistema'
        mensaje = f'Error en client_Delete: {str(e)}'
        messagebox.showerror (title, mensaje)


class Clients:
    def __init__(self, client_firstname, client_lastname, client_ci, client_phone, client_address, client_mail):
        self.id_client = None
        self.client_firstname = client_firstname
        self.client_lastname = client_lastname
        self.client_ci = client_ci
        self.client_phone = client_phone
        self.client_address = client_address
        self.client_mail = client_mail

    def __str__(self):
        return f'Clients[{self.client_firstname}, {self.client_lastname}, {self.client_ci}, {self.client_phone}, {self.client_address}, {self.client_mail}]'
