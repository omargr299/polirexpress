import pyodbc 
import openpyxl
import pandas as pd
from datetime import datetime
import archivo

def conexion(usuario_base:str, contrasena_base:str):
    try:
        CNXN = pyodbc.connect('DRIVER={SQL Server};SERVER=RICARDO-FLORES;DATABASE=poliexpress;UID=' + usuario_base + ';PWD=' + contrasena_base + ';Trusted_Connection=yes;', timeout=50)
        print("Conexión exitosa")
        return CNXN
    except Exception as e:
        print("No se pudo conectar a la base de datos:", e)
        return None


def insertar(cursor, Destino):
    Fecha = datetime.now()
    query = "INSERT INTO registros (Destino,Fecha) VALUES (?, ?)"
    valores = (Destino,Fecha)
    cursor.execute(query, valores)
    cursor.commit()

def refresh(cursor)->list[tuple[int,str,datetime]]:
    
    cursor.execute("SELECT * FROM registros")
    rows = cursor.fetchall()
    return rows

if __name__ == '__main__':
    con = conexion('poliexpress','poliexpress')
    if con is not None:
        datos = refresh(con.cursor())
        archivo.excel(datos)


