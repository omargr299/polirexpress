from os import remove,listdir
import data


estaciones = data.get_estaciones()
carpeta = './ejemplos2/'
for estacion in estaciones: 
    for archivo in listdir(carpeta+estacion):
        
        remove(carpeta+estacion+'/'+archivo)