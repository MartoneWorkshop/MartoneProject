from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice


def SaveDepot(deposito):
    conexion = ConexionDB()
    sql = f"""INSERT INTO deposito (codDep, name_dep, date_created,date_update, activo)
    VALUES('{deposito.codDep}','{deposito.name_dep}','{deposito.date_created}','{deposito.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveDepot, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def SaveGroup(grupo):
    conexion = ConexionDB()
    sql = f"""INSERT INTO grupo (codgrupo, codDep, name_group, date_created, date_update, activo)
    VALUES('{grupo.codgrupo}','{grupo.codDep}','{grupo.name_group}','{grupo.date_created}','{grupo.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveDepot, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def ListarDepositos():
    conexion = ConexionDB()
    ListarDepositos = []
    sql = 'SELECT * FROM deposito WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        ListarDepositos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en ListarDepositos, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return ListarDepositos

def InformacionDeposito(where):
    conexion = ConexionDB()
    listarDeposito = []
    sql = f'SELECT * FROM deposito {where}'
    try:
        conexion.cursor.execute(sql)
        listarDeposito = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en InformacionDeposito, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarDeposito

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
        mensaje = f'Error en ListarGrupos, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return ListarGrupos

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
        mensaje = f'Error en InformacionGrupos, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarGrupo

def DepotDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE deposito SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en DepotDisable, en AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def EditDepot(deposito, id):
    conexion = ConexionDB()
    sql = f"""UPDATE deposito SET name_dep = '{deposito.name_dep}', date_update = '{deposito.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditDepot, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def EditGroup(grupo, id):
    conexion = ConexionDB()
    sql = f"""UPDATE grupo SET name_group = '{grupo.name_group}', date_update = '{grupo.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditGroup, AdjustDepotsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def AsignarDeposito():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, codDep, name_dep FROM deposito"""
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                
                depositos = resultados
                conexion.cerrarConexion()
                return depositos
        except Exception as e:
                error_advice()
                mensaje = f'Error en asignarDeposito, adjustDepotsDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 
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

class Deposito:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'
class Grupo:
    def __init__(self, codgrupo, codDep, name_group, date_created, date_update):
        self.id = None
        self.codgrupo = codgrupo
        self.codDep = codDep
        self.name_group = name_group
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Grupo[{self.codgrupo},{self.codDep}, {self.name_group}, {self.date_created}, {self.date_update}]'

class SubGrupo:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'

