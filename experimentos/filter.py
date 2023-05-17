import cv2
import os
import recorte as rc

def filter(img):
    umbral = 145
    img[img>umbral] = 255
    img[img<=umbral] = 0
    return img

carpeta = 'ejemplos/'
for subcarpeta in os.listdir('ejemplos'):
    for archivo in os.listdir(carpeta+subcarpeta):
        img = cv2.imread(carpeta+subcarpeta+'/'+archivo)
        img = filter(img)
        rc.recorte(img)
        cv2.imshow('img',img)
        print(f'imagen {archivo} procesada')
        cv2.waitKey(50)
