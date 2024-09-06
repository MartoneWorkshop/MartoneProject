from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


def save_depot(deposito):
    conexion = ConexionDB()
    sql = f"""INSERT INTO deposito (codDep, name_dep, date_created,date_update, activo)
    VALUES('{deposito.codDep}','{deposito.name_dep}','{deposito.date_created}','{deposito.date_update}',1)"""
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
    sql = 'SELECT * FROM deposito WHERE activo = 1'

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
    listarDeposito = []
    sql = f'SELECT * FROM deposito {where}'
    try:
        conexion.cursor.execute(sql)
        listarDeposito = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchDepots, DepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarDeposito


def depotDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE deposito SET activo = 0 WHERE id = {id}'
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

def edit_depot(deposito, id):
    conexion = ConexionDB()
    sql = f"""UPDATE deposito SET name_dep = '{deposito.name_dep}', date_update = '{deposito.date_update}', activo = 1 WHERE id = {id}"""
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
    sql = "SELECT * FROM deposito WHERE activo = 1"
    depositos = []

    try:
        conexion.cursor.execute(sql)
        depositos = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f"Error en getDepots, DepotsDao: {str(e)}"
        with open("error_log.txt", "a") as file:
            file.write(mensaje + "\n")

    return depositos

class Deposito:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'
