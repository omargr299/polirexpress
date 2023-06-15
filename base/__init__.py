import pyodbc 

from datetime import datetime


def conexion(usuario_base:str, contrasena_base:str):
    try:
        print("Conectando a la base de datos...")
        CNXN = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-OR5S81E4;DATABASE=poliexpress;UID=' + usuario_base + ';PWD=' + contrasena_base + ';Trusted_Connection: yes;', timeout=50)
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
    
    cursor.execute("SELECT TOP 20 * FROM registros ORDER BY Id DESC")
    rows = cursor.fetchall()
    return rows

def getAll(cursor)->list[tuple[int,str,datetime]]:
    
    cursor.execute("SELECT * FROM registros ORDER BY Id DESC")
    rows = cursor.fetchall()
    return rows

def getEstaciones(cursor):
    cursor.execute("SELECT Ciudad FROM estaciones")
    rows = cursor.fetchall()
    return rows

if __name__ == '__main__':

    con = conexion('poliexpress','poliexpress')
    
    if con is not None:
        datos = getEstaciones(con.cursor())
        print(datos)


