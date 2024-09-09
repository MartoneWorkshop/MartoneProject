from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def edit_supplier(supplier, id):
    conexion = ConexionDB()
    sql = f"""UPDATE suppliers SET nom_fiscal = '{supplier.nom_fiscal}', rif_prov = '{supplier.rif_prov}',
    tipo_per = '{supplier.tipo_per}', telf_prov = '{supplier.telf_prov}',
    dir_fiscal = '{supplier.dir_fiscal}', email_prov = '{supplier.email_prov}', dias_credito = '{supplier.dias_credito}', 
    updated_at = '{supplier.updated_at}', activo = 1 WHERE id = {id}"""
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


def save_supplier(supplier):
    conexion = ConexionDB()
    sql = f"""INSERT INTO suppliers (codProv, nom_fiscal, rif_prov, tipo_per, telf_prov, dir_fiscal, 
    email_prov, dias_credito, created_at, updated_at, activo)
    VALUES('{supplier.codProv}','{supplier.nom_fiscal}','{supplier.rif_prov}','{supplier.tipo_per}',
    '{supplier.telf_prov}','{supplier.dir_fiscal}','{supplier.email_prov}',
    '{supplier.dias_credito}','{supplier.created_at}','{supplier.updated_at}',1)"""
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
    listasupplier = []
    sql = 'SELECT * FROM suppliers WHERE activo = 1'

    try:
        conexion.cursor.execute(sql )
        listasupplier = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listSupplier, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listasupplier

def inactiveSuppliers():
    conexion = ConexionDB()
    listasupplier = []
    sql = f'SELECT * FROM suppliers WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listasupplier = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en inactiveSuppliers, SupplierDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listasupplier    

def searchSupplier(where):
    conexion = ConexionDB()
    listarProveedor = []
    sql = f'SELECT * FROM suppliers {where}'
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
    sql = f'UPDATE suppliers SET activo = 0 WHERE id = {id}'
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



class suppliers:
    def __init__(self, codprov, nom_fiscal, rif_prov, tipo_per, telf_prov, dir_fiscal, email_prov, dias_credito, created_at, updated_at, deleted_at):
        self.id = None
        self.codProv = codprov
        self.nom_fiscal = nom_fiscal
        self.rif_prov = rif_prov
        self.tipo_per = tipo_per
        self.telf_prov = telf_prov
        self.dir_fiscal = dir_fiscal
        self.email_prov = email_prov
        self.dias_credito = dias_credito
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return f'suppliers[{self.codProv}, {self.nom_fiscal}, {self.rif_prov}, {self.tipo_per}, {self.telf_prov}, {self.dir_fiscal}, {self.email_prov}, {self.dias_credito}, {self.created_at}, {self.updated_at}, {self.deleted_at}]'
