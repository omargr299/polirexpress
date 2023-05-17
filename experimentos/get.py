import qr 
from random import randint
import cv2

for j in range(2):
    for i in range(4):
        etiqueta,_ = qr.generate(i,randint(0,9999))
        cv2.imwrite(f'./etiquetas2/etiqueta{i+1}-{j+1}.png',etiqueta)