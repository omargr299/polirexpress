from json import load,dump
from pandas import read_csv

ruta = "configs.json"

def get_data():
    with open(ruta) as archivo:
      # Cargar su contenido y crear un diccionario
      datos = load(archivo)
      return datos
    
def set_data(data:dict):
      # Abir (o crear) un archivo ordenes_nuevo.json 
      # y guardar la nueva versión de la información
      
      with open("configs.json", 'w') as archivo_nuevo:
        dump(data, archivo_nuevo)

def getDetectionConfig():
    datos = get_data()
    return datos["deteccion"]

def getImageConfig():
    datos = get_data()
    return datos["image"]


def getEstaciones():
  estaciones = read_csv('estaciones.csv')
  return estaciones.columns.tolist()

if __name__ == '__main__':
    data = get_data()

    set_data(data)