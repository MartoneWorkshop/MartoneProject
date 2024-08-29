import psycopg2
from tkinter import messagebox

class ConexionDB:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'postgres'
        self.user = 'postgres'
        self.password = 'admin'
        self.port = '5432'
        try:
            self.conexion = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.conexion.cursor()
        except psycopg2.Error as error:
            messagebox.showerror("Error de conexion", f"No se pudo conectar a la base de datos: {str(error)}")
    def cerrarConexion(self):
        self.conexion.commit()
        self.conexion.close()
    def ejecutar_consulta(self, consulta):
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
        except psycopg2.Error as error:
            messagebox.showerror("Error", f"Error en la consulta: {str(error)}")
    
    def ejecutar_consulta_parametros(self, consulta, parametros):
        try:
            self.cursor.execute(consulta, parametros)
            self.conexion.commit()
        except psycopg2.Error as error:
            messagebox.showerror("Error", f"Error en la consulta: {str(error)}")

    def obtener_resultado(self):
        resultado = self.cursor.fetchone()
        return resultado
    
    def obtener_resultados(self):
        resultados = self.cursor.fetchall()
        return resultados