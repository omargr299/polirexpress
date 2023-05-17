from cv2 import waitKey,imshow,imread,cvtColor,COLOR_BGR2GRAY,getRotationMatrix2D,warpAffine
from tensorflow import constant
from tensorflow import keras
from keras.utils import to_categorical
from os import listdir
import qr 
from numpy import array
from random import randint 


def rotar(image,angulo):
    w,h,_ = image.shape
    matrix=getRotationMatrix2D((w//2,h//2),angulo,1)
    rotate=warpAffine(image,matrix,(w,h))
    return rotate

def getset():
    images = []
    clases = []
    
    
    for angulo in range(500):
        clase = randint(0,3)
        serie = randint(0,9999)

        etiqueta,_ = qr.generate(clase,serie)
        rotate = rotar(etiqueta,randint(1,360))

        images.append(rotate)
        clases.append(clase)

    clases = to_categorical(clases)
    images = constant(images,dtype='float32',shape=(len(images),120,120,1))
    clases = constant(clases,dtype='float32',shape=(len(clases),4))
    return [images,clases]

def getset2():
    images = []
    series = []
    
    
    for angulo in range(500):
        serie = randint(0,30000000)
        clase = randint(0,1)

        etiqueta,code= qr.generate(clase,serie)
        rotate = rotar(etiqueta,angulo)
        codesquare = rotate[40:80,40:80]

        images.append(codesquare)
        code = array(code)
        series.append(code)

    images = constant(images,dtype='float32',shape=(len(images),40,40,1))
    series = constant(series,dtype='float32',shape=(len(series),25))
    return [images,series]

if __name__=='__main__':
    x,y1 = getset()
    for i in range(len(x)):
        print(y1[i].numpy())
        serie = x[i][40:80,40:80] 
        imshow('etiqueta',x[i].numpy())
        #imshow('serie',serie.numpy())
        waitKey(0)
        
    