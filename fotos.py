import cv2
import deteccion as dt
import data
from time import sleep

cam = cv2.VideoCapture(2,cv2.CAP_DSHOW)

count = 0
estaciones = data.get_estaciones()
carpeta = './ejemplos2/'
for estacion in estaciones: 
    print(estacion)
    for i in range(5):
        print(5-i,'...')
        ret, frame = cam.read()
        sleep(1)
    count = 0
    etiqueta = None
    while True:
        ret, frame = cam.read()
        if (not ret): continue
        cv2.imshow('cam', frame)
        bordes,_,etiqueta = dt.recorte(frame)
        cv2.imshow('bordes', bordes)
        if(etiqueta is not None): 
            cv2.imshow('etiqueta', etiqueta)
            cv2.imwrite(carpeta + estacion + '/' + str(count) + '.jpg', etiqueta)
            count+=1
            print(count)
        if cv2.waitKey(1) == ord('q') or count >= 500:
            break
    sleep(1)
    