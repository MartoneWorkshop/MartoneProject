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

class Deposito:
    def __init__(self, codDep, name_dep, date_created, date_update):
        self.id = None
        self.codDep = codDep
        self.name_dep = name_dep
        self.date_created = date_created
        self.date_update = date_update
    def __str__(self):
        return f'Deposito[{self.codDep}, {self.name_dep}, {self.date_created}, {self.date_update}]'
