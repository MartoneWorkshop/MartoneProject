from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_supplier(proveedores, id):
    conexion = ConexionDB()
    sql = f"""UPDATE proveedores SET nom_fiscal = '{proveedores.nom_fiscal}', rif_prov = '{proveedores.rif_prov}',
    tipo_per = '{proveedores.tipo_per}', telf_prov = '{proveedores.telf_prov}',
    dir_fiscal = '{proveedores.dir_fiscal}', email_prov = '{proveedores.email_prov}', dias_credito = '{proveedores.dias_credito}', 
    date_update = '{proveedores.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en edit_supplier, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')


def save_supplier(proveedores):
    conexion = ConexionDB()
    sql = f"""INSERT INTO proveedores (codProv, nom_fiscal, rif_prov, tipo_per, telf_prov, dir_fiscal, 
    email_prov, dias_credito, date_created, date_update, activo)
    VALUES('{proveedores.codProv}','{proveedores.nom_fiscal}','{proveedores.rif_prov}','{proveedores.tipo_per}',
    '{proveedores.telf_prov}','{proveedores.dir_fiscal}','{proveedores.email_prov}',
    '{proveedores.dias_credito}','{proveedores.date_created}','{proveedores.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
        
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en save_supplier, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listSupplier():
    conexion = ConexionDB()
    listaProveedores = []
    sql = 'SELECT * FROM proveedores WHERE activo = 1'

    try:
        conexion.cursor.execute(sql )
        listaProveedores = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listSupplier, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaProveedores

def inactiveSuppliers():
    conexion = ConexionDB()
    listaProveedores = []
    sql = f'SELECT * FROM proveedores WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaProveedores = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactiveSuppliers, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaProveedores    

def searchSupplier(where):
    conexion = ConexionDB()
    listarProveedor = []
    sql = f'SELECT * FROM proveedores {where}'
    try:
        conexion.cursor.execute(sql)
        listarProveedor = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchSupplier, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarProveedor

def supplierDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE proveedores SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en supplierDisable, en SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class Proveedores:
    def __init__(self, codprov, nom_fiscal, rif_prov, tipo_per, telf_prov, dir_fiscal, email_prov, dias_credito, date_created, date_update):
        self.id = None
        self.codProv = codprov
        self.nom_fiscal = nom_fiscal
        self.rif_prov = rif_prov
        self.tipo_per = tipo_per
        self.telf_prov = telf_prov
        self.dir_fiscal = dir_fiscal
        self.email_prov = email_prov
        self.dias_credito = dias_credito
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'Proveedores[{self.codProv}, {self.nom_fiscal}, {self.rif_prov}, {self.tipo_per}, {self.telf_prov}, {self.dir_fiscal}, {self.email_prov}, {self.dias_credito}, {self.date_created}, {self.date_update}]'
