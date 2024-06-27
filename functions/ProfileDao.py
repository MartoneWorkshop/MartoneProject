from .conexion import ConexionDB
from tkinter import messagebox
import traceback
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def EditProfile(roles, id):
    conexion = ConexionDB()
    sql = f"""UPDATE roles SET name = '{roles.name}', date_update = '{roles.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditProfile, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def SaveProfile(roles):
    conexion = ConexionDB()
    sql = f"""INSERT INTO roles (name, date_created, date_update, activo)
    VALUES('{roles.name}','{roles.date_created}','{roles.date_update}', 1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveProfile, rolesDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
                        
def ActualizacionPermisos(perfil_id, permisos_seleccionados):
        try:
            LimpiarPermisos(perfil_id)
            GuardarNuevosPermisos(perfil_id, permisos_seleccionados)
            print('actualizacion')
        except Exception as e:
                error_advice()
                mensaje = f'Error en ActualizacionPermisos, ProfileDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')

def LimpiarPermisos(perfil_id):
        try:
            conexion = ConexionDB()
            sql = f"DELETE FROM asigperm WHERE idrol = '{perfil_id}'"
            conexion.ejecutar_consulta(sql)
        except Exception as e:
            error_advice()
            mensaje = f'Error en LimpiarPermisos, ProfileDao: {str(e)}'
            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')

def GuardarNuevosPermisos(perfil_id, permisos_seleccionados):
    try:
        print(perfil_id)
        print(permisos_seleccionados)

        conexion = ConexionDB()
        for codpermiso in permisos_seleccionados:
            sql = f"INSERT INTO asigperm (idrol, codpermiso) VALUES('{perfil_id}', '{codpermiso}')"
            conexion.ejecutar_consulta(sql)
        conexion.cerrarConexion()
        save_advice()
    except Exception as e:
            error_advice()
            mensaje = f'Error en GuardarNuevosPermisos, ProfileDao: {str(e)}'

            mensaje += f'Detalles del error: {traceback.format_exc()}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')


def listarPerfil():
    conexion = ConexionDB()
    listaModulos = []
    sql = 'SELECT * FROM roles WHERE activo = 1'
    try:
        conexion.cursor.execute(sql)
        listaModulos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarPerfil, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaModulos

def clientArchived():
    conexion = ConexionDB()
    listaCliente = []
    sql = f'SELECT * FROM roles WHERE activo = 0'
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

def consulPerfiles(where):
    conexion = ConexionDB()
    listarPerfiles = []
    sql = f'SELECT * FROM roles {where}'
    try:
        conexion.cursor.execute(sql)
        listarPerfiles = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulModulos, ProfileDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarPerfiles

def ProfileDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE roles SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
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
