from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


def save_cat(grupo):
    conexion = ConexionDB()
    sql = f"""INSERT INTO grupo (codgrupo, name_group, date_created, date_update, activo)
    VALUES('{grupo.codgrupo}','{grupo.name_group}','{grupo.date_created}','{grupo.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en SaveDepot, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def catDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE grupo SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en catDisable, en GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def listCategory():
    conexion = ConexionDB()
    listCategory = []
    sql = 'SELECT * FROM grupo WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listCategory = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listCategory, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listCategory
def inactive_cat():
    conexion = ConexionDB()
    listCategory = []
    sql = f'SELECT * FROM grupo WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listCategory = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactive_cat, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listCategory    
def searchCategories(where):
    conexion = ConexionDB()
    listarGrupo = []
    sql = f'SELECT * FROM grupo {where}'
    try:
        conexion.cursor.execute(sql)
        listarGrupo = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchCategories, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarGrupo
def edit_cat(grupo, id):
    conexion = ConexionDB()
    sql = f"""UPDATE grupo SET name_group = '{grupo.name_group}', date_update = '{grupo.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_cat, GruposDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

class Grupo:
    def __init__(self, codgrupo, name_group, date_created, date_update):
        self.id = None
        self.codgrupo = codgrupo
        self.name_group = name_group
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Grupo[{self.codgrupo},{self.name_group}, {self.date_created}, {self.date_update}]'
