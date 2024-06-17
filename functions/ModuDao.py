from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def EditModulo(modulos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE modulos SET name = '{modulos.name}', alias = '{modulos.alias}', codmod = '{modulos.codmod}',
    date_update = '{modulos.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditClient, UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def SaveModulo(modulos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO modulos (name, alias, codmod, date_created, date_update, activo)
    VALUES('{modulos.name}','{modulos.alias}','{modulos.codmod}','{modulos.date_created}','{modulos.date_update}', 1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveModulo, modulosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listarModulos():
    conexion = ConexionDB()
    listaModulos = []
    sql = 'SELECT * FROM modulos WHERE activo = 1'
    try:
        conexion.cursor.execute(sql)
        listaModulos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarModulos, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaModulos

def clientArchived():
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM modulos WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaCliente = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en clientArchived, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaCliente    

def consulModulos(where):
    conexion = ConexionDB()
    listarModulos = []
    sql = f'SELECT * FROM modulos {where}'
    try:
        conexion.cursor.execute(sql)
        listarModulos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulModulos, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarModulos

def ModuloDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE modulos SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en ModuloDisable, en ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class Modulos:
    def __init__(self, name, alias, codmod, date_created, date_update):
        self.id = None
        self.name = name
        self.alias = alias
        self.codmod = codmod
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'Modulos[{self.name}, {self.alias}, {self.codmod}, {self.date_created}, {self.date_update}]'
