from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


def SaveGroup(grupo):
    conexion = ConexionDB()
    sql = f"""INSERT INTO grupo (codgrupo, name_group, date_created, date_update, activo)
    VALUES('{grupo.codgrupo}','{grupo.name_group}','{grupo.date_created}','{grupo.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveDepot, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def GroupDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE grupo SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en GroupDisable, en GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def ListarGrupos():
    conexion = ConexionDB()
    ListarGrupos = []
    sql = 'SELECT * FROM grupo WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        ListarGrupos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en ListarGrupos, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return ListarGrupos

def GruposDesactivados():
    conexion = ConexionDB()
    listaGrupos = []
    sql = f'SELECT * FROM grupo WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaGrupos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en GruposDesactivados, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaGrupos    

def InformacionGrupos(where):
    conexion = ConexionDB()
    listarGrupo = []
    sql = f'SELECT * FROM grupo {where}'
    try:
        conexion.cursor.execute(sql)
        listarGrupo = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en InformacionGrupos, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarGrupo

def EditGroup(grupo, id):
    conexion = ConexionDB()
    sql = f"""UPDATE grupo SET name_group = '{grupo.name_group}', date_update = '{grupo.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditGroup, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def consulCat(where):
    conexion = ConexionDB()
    listarGrupo = []
    sql = f'SELECT * FROM articulo {where}'
    try:
        conexion.cursor.execute(sql)
        listarGrupo = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulCat, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarGrupo

class Grupo:
    def __init__(self, codgrupo, name_group, date_created, date_update):
        self.id = None
        self.codgrupo = codgrupo
        self.name_group = name_group
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Grupo[{self.codgrupo},{self.name_group}, {self.date_created}, {self.date_update}]'
