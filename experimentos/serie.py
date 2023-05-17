from cv2 import imshow,imwrite,waitKey,resize
from numpy import ones

BASE = ones((20,20,1),dtype='float32')*255

def get_serie(num):
    serie = BASE.copy()
    code = bin(num)[2:]
    code = f'{code:0>25}'
    code = code[::-1]
    row = col = 0
    for i in range(len(code)):
        if code[i] == '0':
            serie[row*4:(row+1)*4,col*4:(col+1)*4] = 0
        col += 1
        if col > 4:
            col = 0
            row += 1
            if row > 4:
                row = 0
    code = [int(i) for i in code]
    return [serie,code]
        
if __name__=='__main__':
    #num = int(input('Ingrese un numero: '))
    for i in range(100):
        serie,_ = get_serie(i)
        serie = resize(serie,(80,80))
        imshow('serie',serie)
        waitKey(100) 