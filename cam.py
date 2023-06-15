import cv2
import deteccion as dt
import tensorflow as tf

model = tf.keras.models.load_model('modelo/modelo-1.h5')
model.load_weights('modelo/pesos-1.h5')

cam = cv2.VideoCapture(2,cv2.CAP_DSHOW)
while True:
    etiqueta = None
    estacion=''
    rect, frame = cam.read()

    if rect:
        frame = cv2.resize(frame,(300,300),interpolation = cv2.INTER_AREA)
        contornos,deteccion,etiqueta = dt.recorte(frame)
    
    cv2.imshow("cam",frame)
    if etiqueta is not None:
        cv2.imshow("cam",deteccion)
        cv2.imshow("etiqueta",etiqueta)
        etiqueta = cv2.resize(etiqueta,(120,120),interpolation = cv2.INTER_AREA)
        new = tf.constant(etiqueta,dtype='float32',shape=(1,120,120,1))
        predict = model.predict(new)
        estacion = str(predict.argmax())
        print(estacion)
    if cv2.waitKey(1) == ord("q"):
        break