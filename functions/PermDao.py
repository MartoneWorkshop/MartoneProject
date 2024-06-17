from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def EditPermiso(permisos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE permisos SET name = '{permisos.name}', date_update = '{permisos.date_update}', WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditPermiso, EditPermiso: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def SavePermiso(permisos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO permisos (idmod, name, codperm, date_created, date_update)
    VALUES('{permisos.idmod}','{permisos.name}','{permisos.codperm}','{permisos.date_created}','{permisos.date_update}')"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SavePermiso, permisosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listarPermisos():
    conexion = ConexionDB()
    listaPermisos = []
    sql = 'SELECT * FROM permisos'
    try:
        conexion.cursor.execute(sql)
        listaPermisos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarPermisos, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaPermisos

def clientArchived():
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM permisos WHERE activo = 0'
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

def consulPermisos(where):
    conexion = ConexionDB()
    listarPermisos = []
    sql = f'SELECT * FROM permisos {where}'
    try:
        conexion.cursor.execute(sql)
        listarPermisos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulPermisos, ModuDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarPermisos

def PermisoDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE permisos SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en PermisoDisable, en ModuDao: {str(e)}'
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
        return f'Permisos[{self.idmod}, {self.name},  {self.codperm}, {self.date_created}, {self.date_update}]'
