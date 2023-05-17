import cv2
import numpy as np
import serie

BASE = np.ones((120,120,1),dtype='float32')*255

zero = np.zeros((30,30,1),dtype='float32')
one = zero.copy()
one[5:25,5:25] = 255
szero = np.zeros((20,20,1),dtype='float32')
sone = szero.copy()
sone[5:15,5:15] = 255

def generate(num:int,numserie:int=0):
    etiqueta = BASE.copy()
    
    codeserie,binserie = serie.get_serie(numserie)
    if num>31 or num<0:
        raise 'Numero fuera de rango'

    code = bin(num)[2:]
    code = f'{code:0>5}'

    a,b,c,d,e = [int(i) for i in code]
    etiqueta[10:40,10:40] = zero if a==0 else one
    etiqueta[80:110,10:40] = zero if b==0 else one
    etiqueta[80:110,80:110] = zero if c==0 else one
    etiqueta[10:30,90:110] = szero if d==0 else sone
    etiqueta[35:55,90:110] = szero if e==0 else sone

    etiqueta[50:70,50:70] = codeserie

    etiqueta[45:48,45:60] = 0
    etiqueta[45:60,45:48] = 0
    """ etiqueta[45:48,50:75] = 0
    etiqueta[72:75,45:75] = 0
    etiqueta[50:75,45:48] = 0
    etiqueta[45:75,72:75] = 0 """

    return [etiqueta,binserie]

    

if __name__=='__main__':

    for i in range(32):
        etiqueta,_ = generate(i,1000)
        cv2.imshow('etiqueta',etiqueta)
        series = etiqueta[40:80,40:80]
        series = cv2.resize(series,(80,80))
        cv2.imshow('serie',series)
        cv2.waitKey(100)