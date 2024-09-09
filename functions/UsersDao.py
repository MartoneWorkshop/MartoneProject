from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_user(user, id):
    conexion = ConexionDB()
    sql = f"""UPDATE user SET username = '{user.username}', password = '{user.password}', 
    idrol = '{user.idrol}', updated_at = '{user.updated_at}', activo = 1 WHERE id = {id}"""
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
def save_user(user):
    conexion = ConexionDB()
    sql = f"""INSERT INTO user (coduser, username, password, idrol, created_at, updated_at, activo)
    VALUES('{user.coduser}','{user.username}','{user.password}','{user.idrol}','{user.created_at}','{user.updated_at}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en SaveClient, userDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def listUsers():
    conexion = ConexionDB()
    listaUsuario = []
    sql = 'SELECT * FROM user WHERE activo = 1'

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
    listauser = []
    sql = f'SELECT * FROM user WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listauser = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactive_user, userDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listauser    
def searchUsers(where):
    conexion = ConexionDB()
    listarUsuario = []
    sql = f'SELECT * FROM user {where}'
    try:
        conexion.cursor.execute(sql)
        listarUsuario = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consuluser, UsuarioDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarUsuario
def userDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE user SET activo = 0 WHERE id = {id}'
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
    def __init__(self, coduser, username, password, idrol, created_at, updated_at, deleted_at):
        self.id = None
        self.coduser = coduser
        self.username = username
        self.password = password
        self.idrol = idrol
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return f'user[{self.username}, {self.password}, {self.idrol}, {self.created_at}, {self.updated_at}, {self.deleted_at}]'
