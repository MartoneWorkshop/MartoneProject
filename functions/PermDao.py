from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_permission(permiss, id):
    conexion = ConexionDB()
    sql = f"""UPDATE permiss SET name = '{permiss.name}', updated_at = '{permiss.updated_at}' WHERE id = {id}"""
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

def save_permission(permiss):
    conexion = ConexionDB()
    sql = f"""INSERT INTO permiss (idmod, name, codperm, created_at, updated_at)
    VALUES('{permiss.idmod}','{permiss.name}','{permiss.codperm}','{permiss.created_at}','{permiss.updated_at}')"""
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
    sql = 'SELECT * FROM permiss'
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
    sql = f'SELECT * FROM permiss {where}'
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
    sql = f'DELETE FROM permiss WHERE id = {id}'
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



class permiss:
    def __init__(self, idmod, name, codperm, created_at, updated_at):
        self.id = None
        self.idmod = idmod
        self.name = name
        self.codperm = codperm
        self.created_at = created_at
        self.updated_at = updated_at
    def __str__(self):
        return f'permiss[{self.idmod}, {self.name}, {self.codperm}, {self.created_at}, {self.updated_at}]'
