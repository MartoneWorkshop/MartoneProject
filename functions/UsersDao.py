from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_user(usuarios, id):
    conexion = ConexionDB()
    sql = f"""UPDATE usuarios SET username = '{usuarios.username}', password = '{usuarios.password}', 
    idrol = '{usuarios.idrol}', date_update = '{usuarios.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en EditClient, UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def save_user(usuarios):
    conexion = ConexionDB()
    sql = f"""INSERT INTO usuarios (coduser, username, password, idrol, date_created, date_update, activo)
    VALUES('{usuarios.coduser}','{usuarios.username}','{usuarios.password}','{usuarios.idrol}','{usuarios.date_created}','{usuarios.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en SaveClient, usuariosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def listUsers():
    conexion = ConexionDB()
    listaUsuario = []
    sql = 'SELECT * FROM usuarios WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listaUsuario = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listUsers, UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaUsuario
def inactive_users():
    conexion = ConexionDB()
    listaUsuarios = []
    sql = f'SELECT * FROM usuarios WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaUsuarios = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactive_user, usuariosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaUsuarios    
def searchUsers(where):
    conexion = ConexionDB()
    listarUsuario = []
    sql = f'SELECT * FROM usuarios {where}'
    try:
        conexion.cursor.execute(sql)
        listarUsuario = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulUsuarios, UsuarioDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarUsuario
def userDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE usuarios SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en UserDelete, en UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
class user:
    def __init__(self, coduser, username, password, idrol, date_created, date_update):
        self.id = None
        self.coduser = coduser
        self.username = username
        self.password = password
        self.idrol = idrol
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'user[{self.username}, {self.password}, {self.idrol}, {self.date_created}, {self.date_update}]'
