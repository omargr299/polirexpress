import cv2 
import recorte as rt
img = cv2.imread('./ejemplos/monterrey/97.jpg')
etiqueta = rt.recorte(img)
cv2.imshow('img',img)
cv2.waitKey(0)