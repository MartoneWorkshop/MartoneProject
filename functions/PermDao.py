from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_permission(permisos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE permisos SET name = '{permisos.name}', date_update = '{permisos.date_update}' WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_permission, PermDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def save_permission(permisos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO permisos (idmod, name, codperm, date_created, date_update)
    VALUES('{permisos.idmod}','{permisos.name}','{permisos.codperm}','{permisos.date_created}','{permisos.date_update}')"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en save_permission, PermDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listPermissions():
    conexion = ConexionDB()
    listPerm = []
    sql = 'SELECT * FROM permisos'
    try:
        conexion.cursor.execute(sql)
        listPerm = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listPermissions, PermDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listPerm


def searchPermiss(where):
    conexion = ConexionDB()
    permList = []
    sql = f'SELECT * FROM permisos {where}'
    try:
        conexion.cursor.execute(sql)
        permList = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchPermiss, PermDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return permList

def PermissDelete(id):
    conexion = ConexionDB()
    sql = f'DELETE FROM permisos WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en PermissDelete, en PermDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class Permisos:
    def __init__(self, idmod, name, codperm, date_created, date_update):
        self.id = None
        self.idmod = idmod
        self.name = name
        self.codperm = codperm
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'Permisos[{self.idmod}, {self.name}, {self.codperm}, {self.date_created}, {self.date_update}]'
