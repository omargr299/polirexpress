import cv2
import qr as qr

etiqueta=qr.get_etiqueta(0)
w,h,_=etiqueta.shape
for i in range(1,361):
    matrix=cv2.getRotationMatrix2D((w//2,h//2),i,1)
    rotate=cv2.warpAffine(etiqueta,matrix,(w,h))
    cv2.imshow('etiqueta',rotate)
    cv2.waitKey(10)