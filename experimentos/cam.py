import cv2
import recorte as rec
from tensorflow import constant,round
from numpy import argmax
from tensorflow.python.keras.models import load_model

cam = cv2.VideoCapture(2,cv2.CAP_DSHOW)

model = load_model('modelo/modelo2.h5') #caragamos el modelo
model.load_weights('modelo/pesos2.h5') #cargamos los pesos
while True:
    ret,frame = cam.read()
    cv2.imshow('cam',frame)
    _,_,etiqueta= rec.recorte(frame)
    if etiqueta is not None:
        etiqueta = cv2.resize(etiqueta,(120,120))
        etiqueta = constant(etiqueta,dtype='float32',shape=(1,120,120,1))
        predict = round(model.predict(etiqueta)).numpy()
        print(predict)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break