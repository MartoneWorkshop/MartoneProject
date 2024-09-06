import sqlite3
from tkinter import messagebox

class ConexionDB:
    
    def __init__(self):
        self.baseDatos = 'database/database.db'
        self.conexion = sqlite3.connect(self.baseDatos)
        self.cursor = self.conexion.cursor()

    def closeConexion(self):
        self.conexion.commit()
        self.conexion.close()
        
    def execute_consult(self, consulta):
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error en la consulta: {str(error)}")
            
    def execute_consult_param(self, consulta, parametros):
        try:
            self.cursor.execute(consulta, parametros)
            self.conexion.commit()
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error en la consulta: {str(error)}")
    
    def get_result(self):
        resultado = self.cursor.fetchone()
        return resultado
    
    def get_results(self):
        resultados = self.cursor.fetchall()
        return resultados