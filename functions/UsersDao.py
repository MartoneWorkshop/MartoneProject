from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def EditUser(usuarios, id):
    conexion = ConexionDB()
    sql = f"""UPDATE usuarios SET username = '{usuarios.username}', password = '{usuarios.password}', 
    idrol = '{usuarios.idrol}', date_update = '{usuarios.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditClient, UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')


def SaveUser(usuarios):
    conexion = ConexionDB()
    sql = f"""INSERT INTO usuarios (coduser, username, password, idrol, date_created, date_update, activo)
    VALUES('{usuarios.coduser}','{usuarios.username}','{usuarios.password}','{usuarios.idrol}','{usuarios.date_created}','{usuarios.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveClient, usuariosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listarUsuarios():
    conexion = ConexionDB()
    listaUsuario = []
    sql = 'SELECT * FROM usuarios WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listaUsuario = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarUsuarios, UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaUsuario

def UsuariosDesactivados():
    conexion = ConexionDB()
    listaUsuarios = []
    sql = f'SELECT * FROM usuarios WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaUsuarios = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en UsuariosDesactivados, usuariosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaUsuarios    

def consulUsers(where):
    conexion = ConexionDB()
    listarUsuario = []
    sql = f'SELECT * FROM usuarios {where}'
    try:
        conexion.cursor.execute(sql)
        listarUsuario = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulUsuarios, UsuarioDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarUsuario

def UserDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE usuarios SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en UserDelete, en UsersDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class usuarios:
    def __init__(self, coduser, username, password, idrol, date_created, date_update):
        self.id = None
        self.coduser = coduser
        self.username = username
        self.password = password
        self.idrol = idrol
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'usuarios[{self.username}, {self.password}, {self.idrol}, {self.date_created}, {self.date_update}]'
