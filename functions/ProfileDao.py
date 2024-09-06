from .conexion import ConexionDB
from tkinter import messagebox
import traceback
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_profile(roles, id):
    conexion = ConexionDB()
    sql = f"""UPDATE roles SET name = '{roles.name}', date_update = '{roles.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_profile, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def save_profile(roles):
    conexion = ConexionDB()
    sql = f"""INSERT INTO roles (name, date_created, date_update, activo)
    VALUES('{roles.name}','{roles.date_created}','{roles.date_update}', 1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en save_profile, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
                        
def update_Permiss(perfil_id, permisos_seleccionados):
        try:
            cleanPermiss(perfil_id)
            saveNewPermiss(perfil_id, permisos_seleccionados)
            print('actualizacion')
        except Exception as e:
                error_advice()
                mensaje = f'Error en update_Permiss, ProfileDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')

def cleanPermiss(perfil_id):
        try:
            conexion = ConexionDB()
            sql = f"DELETE FROM asigperm WHERE idrol = '{perfil_id}'"
            conexion.execute_consult(sql)
        except Exception as e:
            error_advice()
            mensaje = f'Error en cleanPermiss, ProfileDao: {str(e)}'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')

def saveNewPermiss(perfil_id, permisos_seleccionados):
    try:
        conexion = ConexionDB()
        for codpermiso in permisos_seleccionados:
            sql = f"INSERT INTO asigperm (idrol, codpermiso) VALUES('{perfil_id}', '{codpermiso}')"
            conexion.execute_consult(sql)
        save_advice()
        conexion.closeConexion()
    except Exception as e:
            error_advice()
            mensaje = f'Error en saveNewPermiss, ProfileDao: {str(e)}'

            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')


def listProfiles():
    conexion = ConexionDB()
    listaPerfiles = []
    sql = 'SELECT * FROM roles WHERE activo = 1'
    try:
        conexion.cursor.execute(sql)
        listaPerfiles = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listProfiles, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaPerfiles

def InactiveProfiles():
    conexion = ConexionDB()
    listarPerfil = []
    sql = f'SELECT * FROM roles WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listarPerfil = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en InactiveProfiles, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarPerfil  

def searchProfiles(where):
    conexion = ConexionDB()
    listarPerfiles = []
    sql = f'SELECT * FROM roles {where}'
    try:
        conexion.cursor.execute(sql)
        listarPerfiles = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchProfiles, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarPerfiles

def ProfileDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE roles SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en ProfileDisable, en ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class Roles:
    def __init__(self, name, date_created, date_update):
        self.id = None
        self.name = name
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'Roles[{self.name}, {self.date_created}, {self.date_update}]'
