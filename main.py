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
    model.predict(constant(zeros(shape=(tam,tam,1)),dtype='float32',shape=(1,tam,tam,1)))

import deteccion as dt
from numpy import argmax
from gui import GUI

def exit(e):
        global loop
        loop = False
        ct.exit()

#creamos la ventana
wnd = GUI("PoliExpress", exit=exit, resizable=True)
def parar(e):
    global move,transportando
    move = False
    transportando = True
    wnd.default_cams()


def continuar(e):
    global move,transportando
    move = True
    transportando = False
wnd.parar.config(command=parar)
#cam = cv2.VideoCapture(1,cv2.CAP_DSHOW)

from data import getEstaciones
estaciones = getEstaciones()

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
    controller.agarraCaja()
    space = 180//4
    print(estacion)
    controller.estacion((space*(int(estacion)+1))-5)
    controller.default()
    move = True
    transportando = False
    controller.banda.mover()


from threading import Thread
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
        wnd.set_etiqueta(estaciones[estacion])
        putText(deteccion,estaciones[estacion],(20,20),FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,LINE_AA)
        wnd.update_screen(deteccion) 

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