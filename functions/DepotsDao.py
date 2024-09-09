from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


def save_depot(deposit):
    conexion = ConexionDB()
    sql = f"""INSERT INTO deposit (codDep, name_dep, created_at, updated_at, activo)
    VALUES('{deposit.codDep}','{deposit.name_dep}','{deposit.created_at}','{deposit.updated_at}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en save_depot, DepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listDepot():
    conexion = ConexionDB()
    listDepot = []
    sql = 'SELECT * FROM deposit WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listDepot = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listDepot, DepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listDepot

def searchDepots(where):
    conexion = ConexionDB()
    listardeposit = []
    sql = f'SELECT * FROM deposit {where}'
    try:
        conexion.cursor.execute(sql)
        listardeposit = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchDepots, DepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listardeposit


def depotDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE deposit SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en DepotDisable, en DepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def edit_depot(deposit, id):
    conexion = ConexionDB()
    sql = f"""UPDATE deposit SET name_dep = '{deposit.name_dep}', updated_at = '{deposit.updated_at}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_depot, DepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def getDepots():
    conexion = ConexionDB()
    sql = "SELECT * FROM deposit WHERE activo = 1"
    deposits = []

    try:
        conexion.cursor.execute(sql)
        deposits = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f"Error en getDepots, DepotsDao: {str(e)}"
        with open("error_log.txt", "a") as file:
            file.write(mensaje + "\n")

    return deposits

class deposit:
    def __init__(self, codDep, name_dep, created_at, updated_at, deleted_at):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    def __str__(self):
        return f'deposit[{self.codDep}, {self.name_dep}, {self.created_at}, {self.updated_at}, {self.deleted_at}]'
