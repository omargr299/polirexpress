from tensorflow.python.keras.models import load_model
from tensorflow import constant,round
from os import path 
from cv2 import imshow,waitKey
from numpy import array

if path.exists('modelo/modelo2.h5'): #Si existe el modelo
    print('Cargando modelo...')
    classmodel = load_model('modelo/modelo2.h5') #caragamos el modelo
    classmodel.load_weights('modelo/pesos2.h5') #cargamos los pesos
    print("modelo cargado")

import sets as gen

total_acc, total_err = 0,0
print('----prueba de estaciones----')
for i in range(30):
    x_set,y1_set = gen.getset()

    clases = classmodel.predict(x_set)
    for i in range(len(clases)):
        predict = round(clases[i]).numpy()
        label = y1_set[i].numpy()
        # print(predict,label,(predict==label).all())

    asserts = (round(clases)==y1_set).numpy().all(axis=1)
    # print(asserts)
    total_acc += asserts.sum()
    total_err += (asserts==False).sum()
    print("aciertos:",asserts.sum(),"|","errores:",(asserts==False).sum())

print("total aciertos: ",total_acc,"total errores: ",total_err)
print("total aciertos: ",total_acc,"total errores: ",total_err)
print("Porcentaje de acierto:",(total_acc/(total_acc+total_err))*100,"%")