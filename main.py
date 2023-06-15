# obtemos la luista de etiquetas que tenemos ejemplos

#Inicializamos la camara
from cv2 import waitKey,resize,cvtColor,INTER_AREA,COLOR_GRAY2BGR,putText,FONT_HERSHEY_SIMPLEX,LINE_AA

#Cargamos el modelo
from tensorflow.python.keras.models import load_model
from tensorflow import constant
from numpy import zeros
from os import path
from data import getImageConfig

tam = getImageConfig()
if path.exists('modelo/modelo-1.h5'): #Si existe el modelo
    print('Cargando modelo...')
    model = load_model('modelo/modelo-1.h5') #caragamos el modelo
    model.load_weights('modelo/pesos-1.h5') #cargamos los pesos
    print("modelo cargado")
    print("incializando modelo...")
    model.predict(constant(zeros(shape=(tam,tam,1)),dtype='float32',shape=(1,tam,tam,1)))
    print("modelo inicializado")
    
import deteccion as dt
from numpy import argmax
from GUI import App

def exit(e):
        global loop
        loop = False
        ct.exit()

#creamos la ventana
wnd = App("PoliExpress", finish=exit, resizable=True)
def parar():
    global move,transportando,controller
    move = False
    transportando = True
    controller.banda.parar()
    wnd.default_cams()

def continuar():
    global move,transportando,controller
    move = True
    transportando = False
    controller.banda.mover()
    
wnd.botones.parar.config(command=parar)
wnd.botones.continuar.config(command=continuar)

from base import getEstaciones
estaciones = getEstaciones(wnd.conex.cursor() )

loop = True

import controller as ct
controller = ct.Controller()
controller.default()
controller.banda.mover()
move = True
transportando = False

def rutine(estacion):
    global move,transportando,controller
    controller.banda.parar()
    controller.agarrarCaja()
    space = 180//4
    print(estacion)
    controller.estacion((space*(int(estacion)+1))-5)
    controller.default()
    move = True
    transportando = False
    controller.banda.mover()


from threading import Thread
from base import insertar
#bucle de deteccion
while loop:
    estacion = ''
    rect, frame = wnd.get_frame() #se lee el frame

    contornos = None
    etiqueta = None
    if rect:
        wnd.update_screen(frame)
        contornos,deteccion,etiqueta=dt.recorte(frame) #se recorta la etiqueta
        rect, frame = wnd.get_frame() #se lee el frame
        wnd.update_screen(frame)
        wnd.update_cams()


    wnd.update_contornos(contornos)
    
    #si se detecto una etiqueta iniciamos el proceso de prediccion
    if etiqueta is not None and move:
        etiqueta = resize(etiqueta,(tam,tam),interpolation = INTER_AREA) #redimensionamos la imagen a 100x100
        wnd.update_etiqueta(cvtColor(etiqueta, COLOR_GRAY2BGR))

        new = constant(etiqueta,dtype='float32',shape=(1,tam,tam,1)) #convertimos a un tensor con la forma de entrada
        prediccion = model.predict(new) #realizamos la prediccion
        

        estacion = argmax(prediccion) #obtenemos el indice de la clase con mayor probabilidad
        wnd.set_etiqueta(estaciones[estacion][0])
        putText(deteccion,estaciones[estacion][0],(20,20),FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,LINE_AA)
        wnd.update_screen(deteccion) 

        insertar(wnd.conex.cursor(),estaciones[estacion][0])
        wnd.tabla.update()

        move=False
        #cv2.putText(frame,clases[clase],(100,100),cv2.FONT_HERSHEY_SIMPLEX,5,(0,0,255),5,cv2.LINE_AA) #mostramos la clase en pantalla
    
    
    #cv2.imshow('frame', frame) #mostramos el frame con la clase detectada

    wnd.update_cams()
    wnd.update_window()
    
    if not transportando and not move:
        transportando=True
        t = Thread(target=rutine,args=(estacion,))
        t.start()
        
    if waitKey(1) & 0xFF == ord('q'): #si se presiona la tecla q se sale del bucle
        break