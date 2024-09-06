from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def getSupplier():
    try:
        conexion = ConexionDB()
        sql = f"""SELECT id, codProv, nom_fiscal FROM proveedores WHERE activo = 1"""
        conexion.execute_consult(sql)
        resultados = conexion.get_results()
        
        depositos = resultados
        conexion.closeConexion()
        return depositos
    except Exception as e:
            error_advice()
            mensaje = f'Error en ObtenerProveedores, ProductDao: {str(e)}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n') 
def getCategory():
    try:
        conexion = ConexionDB()
        sql = f"""SELECT id, codgrupo, name_group FROM grupo WHERE activo = 1"""
        conexion.execute_consult(sql)
        resultados = conexion.get_results()
        
        depositos = resultados
        conexion.closeConexion()
        return depositos
    except Exception as e:
            error_advice()
            mensaje = f'Error en ObtenerGrupos, ProductDao: {str(e)}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')     
def getDepots():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, codDep, name_dep FROM deposito WHERE activo = 1"""
                conexion.execute_consult(sql)
                resultados = conexion.get_results()
                
                depositos = resultados
                conexion.closeConexion()
                return depositos
        except Exception as e:
                error_advice()
                mensaje = f'Error en ObtenerDepositos, ProductDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 

def edit_product(productos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE articulo SET codProducto = '{productos.codProducto}', codDep = '{productos.codDep}',
    codgrupo = '{productos.codgrupo}', codProv = '{productos.codProv}', nombre_producto = '{productos.nombre_producto}',
    marca = '{productos.marca}', modelo = '{productos.modelo}', serial = '{productos.serial}', costo = '{productos.modelo}',
    descripcion = '{productos.descripcion}', date_update = '{productos.date_update}', activo = 1 WHERE id = {id}"""
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


def save_product(productos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO articulo (codProducto, codDep, codgrupo, codProv, nombre_producto,
    marca, modelo, serial, costo, descripcion, date_created, date_update, activo)
    VALUES('{productos.codProducto}','{productos.codDep}','{productos.codgrupo}',
    '{productos.codProv}','{productos.nombre_producto}','{productos.marca}',
    '{productos.modelo}','{productos.serial}','{productos.costo}','{productos.descripcion}','{productos.date_created}','{productos.date_update}',1)"""
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
    listaProductos = []
    sql = 'SELECT * FROM articulo WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listaProductos = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en listProduct, ProvsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaProductos

def product_inactive():
    conexion = ConexionDB()
    listaproductos = []
    sql = f'SELECT * FROM articulo WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaproductos = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        conexion.closeConexion()
        error_advice()
        mensaje = f'Error en product_inactive, ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaproductos    

def searchProducts(where):
    conexion = ConexionDB()
    listarProducto = []
    sql = f'SELECT * FROM articulo {where}'
    try:
        conexion.cursor.execute(sql)
        listarProducto = conexion.cursor.fetchall()
        conexion.closeConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en searchProducts, ProductDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarProducto

def productDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE articulo SET activo = 0 WHERE id = {id}'
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



class Producto:
    def __init__(self, codProducto, codDep, codgrupo, codProv, nombre_producto, 
                marca, modelo, serial, costo, descripcion, date_created, date_update):
        
        self.id = None
        self.codProducto = codProducto
        self.codDep = codDep
        self.codgrupo = codgrupo
        self.codProv = codProv
        self.nombre_producto = nombre_producto
        self.marca = marca
        self.modelo = modelo
        self.serial = serial
        self.costo = costo
        self.descripcion = descripcion
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'Producto[{self.codProducto}, {self.codDep}, {self.codgrupo}, {self.codProv}, {self.nombre_producto}, {self.marca}, {self.modelo}, {self.serial}, {self.costo}, {self.descripcion}, {self.date_created}, {self.date_update}]'
