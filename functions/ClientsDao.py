from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def EditClient(client, id):
    conexion = ConexionDB()
    sql = f"""UPDATE client SET cod_client = '{client.cod_client}', client_firstname = '{client.client_firstname}', client_lastname = '{client.client_lastname}', client_ci = '{client.client_ci}', client_phone = '{client.client_phone}', client_address = '{client.client_address}', client_email = '{client.client_email}','{client.updated_at}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditClient, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def SaveClient(client):
    conexion = ConexionDB()
    sql = f"""INSERT INTO client (cod_client, client_firstname, client_lastname, client_ci, client_phone, client_address, client_email, created_at, update_at, activo)
    VALUES('{client.cod_client}','{client.client_firstname}','{client.client_lastname}','{client.client_ci}','{client.client_phone}','{client.client_address}','{client.client_email}','{client.created_at}','{client.updated_at}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveClient, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listarCliente():
    conexion = ConexionDB()
    listaCliente = []
    sql = 'SELECT * FROM client WHERE activo = 1'
    
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarCliente, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaCliente

def clientesDesactivados():
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM client WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en clientArchived, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaCliente    

def consulClient(where):
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM client {where}'
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulClient, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaCliente

def clientDelete(id):
    conexion = ConexionDB()
    sql = f'UPDATE client SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en client_Delete, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class Client:
    def __init__(self, cod_client, client_firstname, client_lastname, client_ci, client_phone, client_address, client_email):
        self.id = None
        self.cod_client = cod_client
        self.client_firstname = client_firstname
        self.client_lastname = client_lastname
        self.client_ci = client_ci
        self.client_phone = client_phone
        self.client_address = client_address
        self.client_email = client_email

    def __str__(self):
        return f'Client[{self.cod_client}, {self.client_firstname}, {self.client_lastname}, {self.client_ci}, {self.client_phone}, {self.client_address}, {self.client_email}]'
