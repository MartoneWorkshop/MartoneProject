import sqlite3
from functions.conexion import ConexionDB
from util.util_alerts import edit_advice, error_advice, save_advice, set_opacity
def ObtenerModulos():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, name, codmod FROM modulos WHERE activo = 1"""
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                
                modulos = resultados
                conexion.cerrarConexion()
                return modulos
        except Exception as e:
                error_advice()
                mensaje = f'Error en obtenerModulos, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')
def ObtenerPermisosAsignados(perfil_id):
        try:
                conexion = ConexionDB()
                sql = f"SELECT id, idrol, codpermiso FROM asigperm WHERE idrol = '{perfil_id}'"
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                asigperm = []
                for resultado in resultados:
                        permisos = {
                                'id': resultado[0],
                                'idrol': resultado[1],
                                'codpermiso': resultado[2]
                        }
                        asigperm.append(permisos)
                        
                return asigperm
        except Exception as e:
                error_advice()
                mensaje = f'Error en ObtenerPermisosDeModulos, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')

def ObtenerPermisosDeModulos(idmod):
        try:
                conexion = ConexionDB()
                sql = f"SELECT id, idmod, name, codperm FROM permisos WHERE idmod = '{idmod}'"
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                permisos = []
                for resultado in resultados:
                        permiso = {
                                'id': resultado[0],
                                'idmod': resultado[1],
                                'name': resultado[2],
                                'codperm': resultado[3]
                        }
                        permisos.append(permiso)
                        
                if permisos:
                        return permisos
                else:
                        return None
        except Exception as e:
                error_advice()
                mensaje = f'Error en ObtenerPermisosDeModulos, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 
                        
def ObtenerListaDeModulos():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, name, codmod FROM modulos WHERE activo = 1"""
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()

                modulos = []
                for resultado in resultados:
                        modulo = {
                        'id': resultado[0],
                        'name': resultado[1],
                        'codmod': resultado[2]
                        }
                        modulos.append(modulo)

                conexion.cerrarConexion()
                return modulos
        except Exception as e:
                error_advice()
                mensaje = f'Error en obtenerModulos, util_functions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')

def buscarCodigoModulo(dato):
        try:
                conexion = ConexionDB()
                sql = f"SELECT codmod FROM modulos WHERE name = '{dato}'"
                conexion.ejecutar_consulta(sql)    
                resultado = conexion.obtener_resultado()
                conexion.cerrarConexion()
                return resultado[0]
        
        except Exception as e:
                error_advice()
                mensaje = f'Error en buscarCodigoModulo, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')

def actualizarCodigoModulo(dato):
        try:

                codigoModuloActual = buscarCodigoModulo(dato)
                codigoModuloNuevo = codigoModuloActual + 1
                conexion = ConexionDB()
                sql = f"UPDATE modulos SET codmod = '{codigoModuloNuevo}' WHERE name = '{dato}'"
                conexion.ejecutar_consulta(sql)
                conexion.cerrarConexion()
        except Exception as e:
                error_advice()
                mensaje = f'Error en actualizarCodigoModulo, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 

def obtener_permisos(perfil_id):
        try:
                conexion = ConexionDB()
                sql = f"SELECT codpermiso FROM asigperm WHERE idrol = '{perfil_id}'"
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                permisos = []
                for resultado in resultados:
                        permisos.append(resultado[0])
                if permisos:
                        return permisos
                else:
                        return None
        except Exception as e:
                error_advice()
                mensaje = f'Error en obtener_permisos, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 
def ObtenerRoles():
        try:
                conexion = ConexionDB()
                sql = f"""SELECT id, name FROM roles"""
                conexion.ejecutar_consulta(sql)
                resultados = conexion.obtener_resultados()
                
                roles = resultados
                conexion.cerrarConexion()
                return roles
        except Exception as e:
                error_advice()
                mensaje = f'Error en obtenerRoles, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n') 
def buscarCorrelativo(dato):
        try:
                conexion = ConexionDB()
                sql = f"SELECT valor FROM correlativo WHERE name = '{dato}'"
                conexion.ejecutar_consulta(sql)    
                resultado = conexion.obtener_resultado()
                conexion.cerrarConexion()
                return resultado[0]
        
        except Exception as e:
                error_advice()
                mensaje = f'Error en buscarCorrelativo, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')
def actualizarCorrelativo(dato):
        try:

                correlativoActual = buscarCorrelativo(dato)
                correlativoNuevo = correlativoActual + 1
                conexion = ConexionDB()
                sql = f"UPDATE correlativo SET valor = '{correlativoNuevo}' WHERE name = '{dato}'"
                conexion.ejecutar_consulta(sql)
                conexion.cerrarConexion()
        except Exception as e:
                error_advice()
                mensaje = f'Error en actualizarCorrelativo, util_funtions: {str(e)}'
                with open('error_log.txt', 'a') as file:
                        file.write(mensaje + '\n')