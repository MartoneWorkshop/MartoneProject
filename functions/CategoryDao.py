from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


def save_cat(category):
    conexion = ConexionDB()
    sql = f"""INSERT INTO category (id_cat, name_category, created_at, updated_at, activo)
    VALUES('{category.id_cat}','{category.name_category}','{category.created_at}','{category.updated_at}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en SaveDepot, categorysDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def catDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE category SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en catDisable, en categorysDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def listCategory():
    conexion = ConexionDB()
    listCategory = []
    sql = 'SELECT * FROM category WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listCategory = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listCategory, categorysDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listCategory
def inactive_cat():
    conexion = ConexionDB()
    listCategory = []
    sql = f'SELECT * FROM category WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listCategory = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactive_cat, categorysDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listCategory    
def searchCategories(where):
    conexion = ConexionDB()
    listarcategory = []
    sql = f'SELECT * FROM category {where}'
    try:
        conexion.cursor.execute(sql)
        listarcategory = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchCategories, categorysDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarcategory
def edit_cat(category, id):
    conexion = ConexionDB()
    sql = f"""UPDATE category SET name_category = '{category.name_category}', updated_at = '{category.updated_at}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_cat, categorysDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

class category:
    def __init__(self, id_cat, name_category, created_at, updated_at, deleted_at):
        self.id = None
        self.id_cat = id_cat
        self.name_category = name_category
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    def __str__(self):
        return f'category[{self.id_cat},{self.name_category}, {self.created_at}, {self.updated_at},{self.deleted_at}]'
