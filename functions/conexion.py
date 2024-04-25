import sqlite3
from tkinter import messagebox

class ConexionDB:
    def __init__(self):
        self.baseDatos = 'database/database.db'
        self.conexion = sqlite3.connect(self.baseDatos)
        self.cursor = self.conexion.cursor()

    def cerrarConexion(self):
        self.conexion.commit()
        self.conexion.close()
        
    def ejecutar_consulta(self, consulta):
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error en la consulta: {str(error)}")

    def obtener_resultado(self):
        resultado = self.cursor.fetchone()
        return resultado