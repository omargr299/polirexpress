
from tensorflow import constant
from tensorflow import keras
from keras.utils import to_categorical
from cv2 import imshow, waitKey,imread,getRotationMatrix2D,warpAffine,cvtColor,COLOR_BGR2GRAY,resize
from os import listdir
from data import get_data,get_estaciones
from random import randint

# funcion para generar datasets de imagenes con deformaciones
def generate():
    carpeta = './etiquetas/' # carpeta donde se guardaran las imagenes
    extension = '.png' # extension de las imagenes
    tam = get_data()["image"]

    labels = get_estaciones()

    imagenes=[]
    clases=[]
    num_etiq = len(labels) # obtenemos la cantidad de etiquetas
    for i in range(400):
        index = randint(0,num_etiq-1) # obtenemos un indice aleatorio
        img = imread(carpeta+labels[index]+extension) # obtenemos una imagen aleatoria
        img = cvtColor(img,COLOR_BGR2GRAY) # convertimos la imagen a escala de grises

        w,h = img.shape[:2] # obtenemos el ancho y alto de la imagen
        matrix = getRotationMatrix2D((w//2,h//2),randint(0,360),1) # obtenemos la matriz de rotacion
        img = warpAffine(img,matrix,(w,h)) # rotamos la imagen

        imagenes.append(img) # agregamos la imagen a la lista de imagenes
        clases.append(index) # agregamos el indice de la etiqueta a la lista de clases
    
    clases = to_categorical(clases) # convertimos las clases a one hot encoding
    imagenes = constant(imagenes,dtype='float32',shape=(len(imagenes),tam,tam,1)) # convertimos las imagenes a un tensor
    clases = constant(clases,dtype='float32',shape=(len(clases),num_etiq)) # convertimos las clases a un tensor

    return (imagenes,clases) # retornamos el el dataset de imagenes

def filter(img):
    umbral = 180
    img[img>umbral] = 255
    img[img<=umbral] = 0
    return img

def generateReal():
    carpeta = './ejemplos2/'
    
    imagenes=[]
    clases=[]

    tam = 120

    labels = get_estaciones()
    num_etiq = len(labels)
    for estacion in listdir(carpeta):

        for foto in listdir(carpeta+estacion):
            img = imread(carpeta+estacion+'/'+foto)
            img = resize(img,(tam,tam))
            img = cvtColor(img,COLOR_BGR2GRAY)
            w,h = img.shape[:2] # obtenemos el ancho y alto de la imagen
            matrix = getRotationMatrix2D((w//2,h//2),randint(1,360),1) # obtenemos la matriz de rotacion
            img = warpAffine(img,matrix,(w,h)) # rotamos la imagen

            #img = filter(img)
            imagenes.append(img)
            clases.append(labels.index(estacion))

    clases = to_categorical(clases)
    imagenes = constant(imagenes,dtype='float32',shape=(len(imagenes),tam,tam,1))
    clases = constant(clases,dtype='float32',shape=(len(clases),num_etiq))

    return (imagenes,clases)
        
if __name__=='__main__': # prueba del generador
    #generateReal()

    imagenes,clases = generateReal()

    # visualizamos las imagenes
    for i in range(len(imagenes)):
        print("imagen",i)
        print(clases[i].numpy())

        imshow('imagen',imagenes[i].numpy())
        
        if waitKey(50) & 0xFF == ord('q'): #si se presiona la tecla q se sale del bucle
            break
