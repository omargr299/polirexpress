import cv2
import data
delay = 1 # tiempo de espera para mostrar la imagen

def show(image): # funcion para mostrar la imagen
    cv2.imshow('Imagen', image)
    cv2.waitKey(delay)



def recorte(imagen): # funcion para recortar la etiqueta
    
    config = data.getDetectionConfig() # obtenemos la configuracion de deteccion
    etiqueta = None # la etiqueta se inicializa en None (osea nada)

    imagen = cv2.resize(imagen,(300,300),interpolation = cv2.INTER_AREA) # redimensionamos la imagen

    # hacemos una copia de la imagen original
    copia = imagen.copy()
    # show(imagen)

    # convertimos la imagen a blanco y negro
    imagen = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
    gray = imagen
    # show(imagen)

    # le aplicamos un desfonque a la imagen
    imagen = cv2.GaussianBlur(imagen,(5,5),0)
    #show(imagen)

    # detectamos todos los bordes
    imagen = cv2.Canny(imagen,100,200)
    #show(imagen)
    
    # obtemos todos los contornos que detectamos los contornos
    (contornos,_) = cv2.findContours(imagen.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos: # revismamos cada uno de los contornos
        #momentos = cv2.moments(c)
        area = cv2.contourArea(c) # obtemos el area que crean los contornos
        (x,y,w,h) = cv2.boundingRect(c) # obtemos las coordenadas de los contornos en la imagen 
        epsilon = 0.09*cv2.arcLength(c,True) # calculo del perimetro
        approx = cv2.approxPolyDP(c,epsilon,True) # numero de lados
    
        if area>config["area"] and len(approx)==config["lados"]: # si el area y el numero de ladops son los correctos
            print('area=',area,'lados=',len(approx))

            aspect_ratio = float(w)/h # calculamos el aspect ratio
            print('aspect ratio=',aspect_ratio)

            if aspect_ratio>config["aspect_ratio"]: # si el aspect ratio es el correcto
                # dibujamos los contornos
                copia = cv2.drawContours(copia,[approx],-1,(0,255,0),3)
                #show(copia)
                #obtenemos la etiqueta
                etiqueta = gray[y:y+h,x:x+w]
                #cv2.imshow('Etiqueta',etiqueta) 
    return [imagen,copia,etiqueta]
    

# prueba con una imagen estatica

if __name__ == '__main__':
    imagen = cv2.imread('./pruebas/prueba5.jpg')
    print(imagen.shape)
    recorte(imagen)
    cv2.waitKey()

