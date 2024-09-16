from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def getSupplier():
    try:
        conexion = ConexionDB()
        sql = f"""SELECT id, codProv, nom_fiscal FROM suppliers WHERE activo = 1"""
        conexion.execute_consult(sql)
        resultados = conexion.get_results()
        
        depositos = resultados
        conexion.closeConexion()
        return depositos
    except Exception as e:
            error_advice()
            mensaje = f'Error en getSupplier, ProductDao: {str(e)}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n') 
def getCategory():
    try:
        conexion = ConexionDB()
        sql = f"""SELECT id, name_category FROM category WHERE activo = 1"""
        conexion.execute_consult(sql)
        resultados = conexion.get_results()
        
        depositos = resultados
        conexion.closeConexion()
        return depositos
    except Exception as e:
            error_advice()
            mensaje = f'Error en getCategory, ProductDao: {str(e)}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')     
def getDepots():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, codDep, name_dep FROM deposit WHERE activo = 1"""
                conexion.execute_consult(sql)
                resultados = conexion.get_results()
                
                depositos = resultados
                conexion.closeConexion()
                return depositos
        except Exception as e:
                error_advice()
                mensaje = f'Error en getDepots, ProductDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 
def edit_product(product, id):
    conexion = ConexionDB()
    sql = f"""UPDATE product SET codProducto = '{product.codProducto}', codDep = '{product.codDep}',
    id_cat = '{product.id_cat}', codProv = '{product.codProv}', nombre_producto = '{product.nombre_producto}',
    marca = '{product.marca}', modelo = '{product.modelo}', serial = '{product.serial}', costo = '{product.costo}',
    descripcion = '{product.descripcion}', updated_at = '{product.updated_at}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        edit_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en EditArt, ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def save_product(product):
    conexion = ConexionDB()
    sql = f"""INSERT INTO product (codProducto, codDep, id_cat, codProv, nombre_producto,  
    marca, modelo, serial, costo,  descripcion, created_at, updated_at, activo)
    VALUES('{product.codProducto}','{product.codDep}','{product.id_cat}','{product.codProv}','{product.nombre_producto}',
    '{product.marca}','{product.modelo}','{product.serial}','{product.costo}','{product.descripcion}','{product.created_at}','{product.updated_at}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        save_advice()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en save_product, ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
def listProduct():
    conexion = ConexionDB()
    listaproduct = []
    sql = 'SELECT * FROM product WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listaproduct = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listProduct, ProvsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaproduct
def product_inactive():
    conexion = ConexionDB()
    listaproduct = []
    sql = f'SELECT * FROM product WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaproduct = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en product_inactive, ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaproduct    

def searchProducts(where):
    conexion = ConexionDB()
    listarproduct = []
    sql = f'SELECT * FROM product {where}'
    try:
        conexion.cursor.execute(sql)
        listarproduct = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchProducts, ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarproduct

def productDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE product SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.closeConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.closeConexion()
        mensaje = f'Error en productDisable, en ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
class product:
    def __init__(self, codProducto, codDep, id_cat, codProv, nombre_producto, 
                marca, modelo, serial, costo, descripcion, created_at, updated_at, deleted_at):
        
        self.id = None
        self.codProducto = codProducto
        self.codDep = codDep
        self.id_cat = id_cat
        self.codProv = codProv
        self.nombre_producto = nombre_producto
        self.marca = marca
        self.modelo = modelo
        self.serial = serial
        self.costo = costo
        self.descripcion = descripcion
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        
    def __str__(self):
        return f'product[{self.codProducto}, {self.codDep}, {self.id_cat}, {self.codProv}, {self.nombre_producto}, {self.marca}, {self.modelo}, {self.serial}, {self.costo}, {self.descripcion}, {self.created_at}, {self.updated_at}, {self.deleted_at}]'
