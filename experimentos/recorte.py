import cv2

delay = 1 # tiempo de espera para mostrar la imagen



def show(image): # funcion para mostrar la imagen
    cv2.imshow('Imagen', image)
    cv2.waitKey(delay)


def recorte(imagen): # funcion para recortar la etiqueta
    minus = None
    etiqueta = None # la etiqueta se inicializa en None (osea nada)

    imagen = cv2.resize(imagen,(300,300),interpolation = cv2.INTER_AREA) # redimensionamos la imagen
    print(imagen.shape)

    # hacemos una copia de la imagen original
    copia = imagen
    original = imagen
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
    show(imagen)
    
    # obtemos todos los contornos que detectamos los contornos
    (contornos,jerarquia) = cv2.findContours(imagen.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos: # revismamos cada uno de los contornos
        #momentos = cv2.moments(c)
        area = cv2.contourArea(c) # obtemos el area que crean los contornos
        (x,y,w,h) = cv2.boundingRect(c) # obtemos las coordenadas de los contornos en la imagen 
        epsilon = 0.09*cv2.arcLength(c,True) # calculo del perimetro
        approx = cv2.approxPolyDP(c,epsilon,True) # numero de lados

        if  area>5000 and len(approx)==4: # si el area y el numero de ladops son los correctos
            print('area=',area,'approx=',len(approx))

            aspect_ratio = float(w)/h # calculamos el aspect ratio
            print('aspect ratio=',aspect_ratio)

            if aspect_ratio>.5: # si el aspect ratio es el correcto
                
                # dibujamos los contornos
                copia = cv2.drawContours(copia,[approx],-1,(0,255,0),3)
                show(copia)
                #obtenemos la etiqueta
                etiqueta = gray[y:y+h,x:x+w]
                cv2.imshow('Etiqueta',etiqueta) 

    print(minus)
    return [imagen,copia,etiqueta]