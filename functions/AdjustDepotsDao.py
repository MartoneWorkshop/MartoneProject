from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def obtener_depositos():
    conexion = ConexionDB()
    sql = "SELECT * FROM deposito WHERE activo = 1"
    depositos = []

    try:
        conexion.cursor.execute(sql)
        depositos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f"Error en obtener_depositos, AdjustDepotsDao: {str(e)}"
        with open("error_log.txt", "a") as file:
            file.write(mensaje + "\n")

    return depositos

def obtener_grupos(codDep):
    conexion = ConexionDB()
    sql = "SELECT * FROM grupo WHERE codDep = ?"
    groups = []

    try:
        conexion.cursor.execute(sql, (codDep,))
        groups = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f"Error en obtener_grupos, AdjustDepotsDao: {str(e)}"
        with open("error_log.txt", "a") as file:
            file.write(mensaje + "\n")

    return groups

def obtener_subgrupos(codgrupo):
    conexion = ConexionDB()
    sql = "SELECT * FROM subgrupo WHERE codgrupo = ?"
    subgroups = []

    try:
        conexion.cursor.execute(sql, (codgrupo,))
        subgroups = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f"Error en obtener_subgrupos, AdjustDepotsDao: {str(e)}"
        with open("error_log.txt", "a") as file:
            file.write(mensaje + "\n")

    return subgroups
class Grupo:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'

class SubGrupo:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'
class Deposito:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'
