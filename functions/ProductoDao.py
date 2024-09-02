from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice

def ObtenerProveedores():
    try:
        conexion = ConexionDB()
        sql = f"""SELECT id, codProv, nom_fiscal FROM proveedores WHERE activo = 1"""
        conexion.ejecutar_consulta(sql)
        resultados = conexion.obtener_resultados()
        
        depositos = resultados
        conexion.cerrarConexion()
        return depositos
    except Exception as e:
            error_advice()
            mensaje = f'Error en ObtenerProveedores, ProductosDao: {str(e)}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n') 
def ObtenerGrupos():
    try:
        conexion = ConexionDB()
        sql = f"""SELECT id, codgrupo, name_group FROM grupo WHERE activo = 1"""
        conexion.ejecutar_consulta(sql)
        resultados = conexion.obtener_resultados()
        
        depositos = resultados
        conexion.cerrarConexion()
        return depositos
    except Exception as e:
            error_advice()
            mensaje = f'Error en ObtenerGrupos, ProductosDao: {str(e)}'
            with open('error_log.txt', 'a') as file:
                    file.write(mensaje + '\n')     
def ObtenerDepositos():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, codDep, name_dep FROM deposito WHERE activo = 1"""
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                
                depositos = resultados
                conexion.cerrarConexion()
                return depositos
        except Exception as e:
                error_advice()
                mensaje = f'Error en ObtenerDepositos, ProductosDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 

def EditArt(productos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE articulo SET codProducto = '{productos.codProducto}', codDep = '{productos.codDep}',
    codgrupo = '{productos.codgrupo}', codProv = '{productos.codProv}', nombre_producto = '{productos.nombre_producto}',
    marca = '{productos.marca}', modelo = '{productos.modelo}', serial = '{productos.serial}', costo = '{productos.modelo}',
    descripcion = '{productos.descripcion}', date_update = '{productos.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditArt, ProductosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')


def SaveArt(productos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO articulo (codProducto, codDep, codgrupo, codProv, nombre_producto,
    marca, modelo, serial, costo, descripcion, date_created, date_update, activo)
    VALUES('{productos.codProducto}','{productos.codDep}','{productos.codgrupo}',
    '{productos.codProv}','{productos.nombre_producto}','{productos.marca}',
    '{productos.modelo}','{productos.serial}','{productos.costo}','{productos.descripcion}','{productos.date_created}','{productos.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveArt, ProductosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listarProductos():
    conexion = ConexionDB()
    listaProductos = []
    sql = 'SELECT * FROM articulo WHERE activo = 1'

    try:
        conexion.cursor.execute(sql)
        listaProductos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarProductos, ProvsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaProductos

def productosDesactivados():
    conexion = ConexionDB()
    listaproductos = []
    sql = f'SELECT * FROM articulo WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaproductos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en productosDesactivados, ProductosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaproductos    

def consulArt(where):
    conexion = ConexionDB()
    listarProducto = []
    sql = f'SELECT * FROM articulo {where}'
    try:
        conexion.cursor.execute(sql)
        listarProducto = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulArt, ProductosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarProducto

def ArtDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE articulo SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en ArtDisable, en ProductosDao: {str(e)}'
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
