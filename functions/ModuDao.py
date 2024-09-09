from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_module(modules, id):
    conexion = ConexionDB()
    sql = f"""UPDATE modules SET name = '{modules.name}', alias = '{modules.alias}', codmod = '{modules.codmod}',
    updated_at = '{modules.updated_at}', activo = 1 WHERE id = {id}"""
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

def save_module(modules):
    conexion = ConexionDB()
    sql = f"""INSERT INTO modules (name, alias, codmod, created_at, updated_at, activo)
    VALUES('{modules.name}','{modules.alias}','{modules.codmod}','{modules.created_at}','{modules.updated_at}', 1)"""
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
    listamodules = []
    sql = 'SELECT * FROM modules WHERE activo = 1'
    try:
        conexion.cursor.execute(sql)
        listamodules = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listModules, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listamodules

def inactive_modules():
    conexion = ConexionDB()
    moduleList = []
    sql = f'SELECT * FROM modules WHERE activo = 0'
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
    sql = f'SELECT * FROM modules {where}'
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
    sql = f'UPDATE modules SET activo = 0 WHERE id = {id}'
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



class modules:
    def __init__(self, name, alias, codmod, created_at, updated_at, deleted_at):
        self.id = None
        self.name = name
        self.alias = alias
        self.codmod = codmod
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return f'modules[{self.name}, {self.alias}, {self.codmod}, {self.created_at}, {self.updated_at}, {self.deleted_at}]'
