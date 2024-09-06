from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_module(modulos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE modulos SET name = '{modulos.name}', alias = '{modulos.alias}', codmod = '{modulos.codmod}',
    date_update = '{modulos.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_module, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def save_module(modulos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO modulos (name, alias, codmod, date_created, date_update, activo)
    VALUES('{modulos.name}','{modulos.alias}','{modulos.codmod}','{modulos.date_created}','{modulos.date_update}', 1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en SaveModulo, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listModules():
    conexion = ConexionDB()
    listaModulos = []
    sql = 'SELECT * FROM modulos WHERE activo = 1'
    try:
        conexion.cursor.execute(sql)
        listaModulos = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listModules, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaModulos

def inactive_modules():
    conexion = ConexionDB()
    moduleList = []
    sql = f'SELECT * FROM modulos WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        moduleList = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactive_modules, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return moduleList    

def searchModules(where):
    conexion = ConexionDB()
    moduleList = []
    sql = f'SELECT * FROM modulos {where}'
    try:
        conexion.cursor.execute(sql)
        moduleList = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchModules, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return moduleList

def moduleDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE modulos SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en moduleDisable, en ModuDao: {str(e)}'
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
