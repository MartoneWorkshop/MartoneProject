from .conexion import ConexionDB
from tkinter import messagebox
from util.util_alerts import save_advice, edit_advice, error_advice, delete_advice
def ObtenerDepositos():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, name_dep FROM deposito WHERE activo = 1"""
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                
                depositos = resultados
                conexion.cerrarConexion()
                return depositos
        except Exception as e:
                error_advice()
                mensaje = f'Error en ObtenerDepositos, ArticulosDao: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 

def EditArt(articulos, id):
    conexion = ConexionDB()
    sql = f"""UPDATE articulo SET codDep = '{articulos.codDep}', codGrupo = '{articulos.codGrupo}',
    codsubGrupo = '{articulos.codsubGrupo}', codProv = '{articulos.codProv}', nombre_producto = '{articulos.nombre_producto}',
    descripcion = '{articulos.descripcion}', marca = '{articulos.marca}', modelo = '{articulos.modelo}', 
    date_update = '{articulos.date_update}', activo = 1 WHERE id = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        edit_advice()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en EditArt, ArticulosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')


def SaveArt(articulos):
    conexion = ConexionDB()
    sql = f"""INSERT INTO articulo (codProv, codDep, codGrupo, codsubGrupo, codProv, nombre_producto, descripcion, 
    marca, modelo, date_created, date_update, activo)
    VALUES('{articulos.codProv}','{articulos.codDep}','{articulos.codGrupo}','{articulos.codsubGrupo}',
    '{articulos.codProv}','{articulos.nombre_producto}','{articulos.descripcion}','{articulos.marca}',
    '{articulos.modelo}','{articulos.date_created}','{articulos.date_update}',1)"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        save_advice()
        
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en SaveProv, ArticulosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')

def listarArticulos():
    conexion = ConexionDB()
    listaArticulos = []
    sql = 'SELECT * FROM articulo WHERE activo = 1'

    try:
        conexion.cursor.execute(sql )
        listaArticulos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en listarArticulos, ProvsDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaArticulos

def articulosDesactivados():
    conexion = ConexionDB()
    listaarticulos = []
    sql = f'SELECT * FROM articulo WHERE activo = 0'
    try:
        conexion.cursor.execute(sql)
        listaarticulos = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        conexion.cerrarConexion()
        error_advice()
        mensaje = f'Error en articulosDesactivados, ArticulosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listaarticulos    

def consulArt(where):
    conexion = ConexionDB()
    listarArticulo = []
    sql = f'SELECT * FROM articulo {where}'
    try:
        conexion.cursor.execute(sql)
        listarArticulo = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except Exception as e:
        error_advice()
        mensaje = f'Error en consulArt, ArticulosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')
    return listarArticulo

def ProvDisable(id):
    conexion = ConexionDB()
    sql = f'UPDATE articulo SET activo = 0 WHERE id = {id}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        delete_advice()

    except Exception as e:
        error_advice()
        conexion.cerrarConexion()
        mensaje = f'Error en ProvDelete, en ArticulosDao: {str(e)}'
        with open('error_log.txt', 'a') as file:
            file.write(mensaje + '\n')



class Articulos:
    def __init__(self, codProducto, codDep, codGrupo, codsubGrupo, codProv, nombre_producto, descripcion, 
                marca, modelo, serial, existencia, lote, fecha_vencimiento, costo, descuento, iva,
                estante, division, date_created, date_update):
        
        self.id = None
        self.codProducto = codProducto
        self.codDep = codDep
        self.codGrupo = codGrupo
        self.codsubGrupo = codsubGrupo
        self.codProv = codProv
        self.nombre_producto = nombre_producto
        self.descripcion = descripcion
        self.marca = marca
        self.modelo = modelo
        self.serial = serial
        self.existencia = existencia
        self.lote = lote
        self.fecha_vencimiento = fecha_vencimiento
        self.costo = costo
        self.descuento = descuento
        self.iva = iva
        self.estante = estante
        self.division = division
        self.date_created = date_created
        self.date_update = date_update

    def __str__(self):
        return f'Articulos[{self.codProducto}, {self.codDep}, {self.codGrupo}, {self.codProv}, {self.codGrupo}, {self.codsubGrupo}, {self.codProv}, {self.nombre_producto}, {self.descripcion}, {self.marca}, {self.modelo}, {self.serial}, {self.existencia}, {self.lote}, {self.fecha_vencimiento}, {self.costo}, {self.descuento}, {self.iva}, {self.estante}, {self.division}, {self.date_created}, {self.date_update}]'
