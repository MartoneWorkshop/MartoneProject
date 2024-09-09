from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_client(client, id):
    conexion = ConexionDB()
    sql = f"""UPDATE client SET client_firstname = '{client.client_firstname}', client_lastname = '{client.client_lastname}', client_ci = '{client.client_ci}', client_phone = '{client.client_phone}', client_address = '{client.client_address}', client_email = '{client.client_email}','{client.updated_at}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en editClient, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def save_client(client):
    conexion = ConexionDB()
    sql = f"""INSERT INTO client (client_firstname, client_lastname, client_ci, client_phone, client_address, client_email, created_at, update_at, activo)
    VALUES('{client.client_firstname}','{client.client_lastname}','{client.client_ci}','{client.client_phone}','{client.client_address}','{client.client_email}','{client.created_at}','{client.updated_at}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en SaveClient, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
            
def listClient():
    conexion = ConexionDB()
    listaCliente = []
    sql = 'SELECT * FROM client WHERE activo = 1'
    
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listClient, ClientsDao: {str(e)}'
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
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en clientArchived, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaCliente    

def searchClients(where):
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM client {where}'
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.closeConexion()
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
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en client_Delete, ClientsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

class client:
    def __init__(self, client_firstname, client_lastname, client_ci, client_phone, client_address, client_email, created_at, updated_at, deleted_at):
        self.id = None
        self.client_firstname = client_firstname
        self.client_lastname = client_lastname
        self.client_ci = client_ci
        self.client_phone = client_phone
        self.client_address = client_address
        self.client_email = client_email
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return f'client[{self.client_firstname}, {self.client_lastname}, {self.client_ci}, {self.client_phone}, {self.client_address}, {self.client_email},{self.created_at}, ,{self.updated_at}, ,{self.deleted_at}]'
