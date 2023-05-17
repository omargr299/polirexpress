from os import path
from tensorflow.python.keras.models import load_model
from tensorflow import constant,round
from time import sleep

def bin_to_dec(bina):
    pos = 0
    deca = 0
    for bit in bina:
        deca += bit*(2**pos)
        pos+=1
    return deca
if path.exists('modelo/modelo3-2.h5'): #Si existe el modelo
    print('Cargando modelo...')
    seriesmodel = load_model('modelo/modelo3-2.h5') #caragamos el modelo
    seriesmodel.load_weights('modelo/pesos3-2.h5') #cargamos los pesos
    print("modelo cargado")

total_acc, total_err = 0,0
print('----prueba de serie----')

import sets as gen


for i in range(10):
    x_set,y2_set = gen.getset2()

    clases = seriesmodel.predict(x_set)
    for i in range(len(clases)):
        predict = round(clases[i]).numpy()
        label = y2_set[i].numpy()
        #print(bin_to_dec(predict),bin_to_dec(label))
    #print(((predict==label).sum()/25)*100,"%")

    asserts = (round(clases)==y2_set).numpy().all(axis=1)
    # print(asserts)
    total_acc += asserts.sum()
    total_err += (asserts==False).sum()
    print("aciertos: ",asserts.sum(),"errores: ",(asserts==False).sum())

print("total aciertos: ",total_acc,"total errores: ",total_err)
print("Porcentaje de acierto:",(total_acc/(total_acc+total_err))*100,"%")