import pyfirmata
import keyboard as ky
from time import sleep

class Banda:
    def __init__(self) -> None:
        self.motor = board.get_pin('d:4:o')

    def mover(self):
        self.motor.write(1)

    def parar(self):
        self.motor.write(0)

class Brazo:
    def __init__(self):
        self.garra = board.get_pin('d:9:s')
        self.incUp = board.get_pin('d:10:s')
        self.incDown = board.get_pin('d:11:s')
        self.giro = board.get_pin('d:12:s')

        
    def volver(self):
        self.giro.write(8)

    def mover(self,grado):
        self.giro.write(grado)

    def cerrar(self):
        self.garra.write(40)

    def agarrar(self):
        self.garra.write(50)
    
    def soltar(self):
        self.garra.write(120)

    def levantar(self):
        self.incUp.write(80)
        self.incDown.write(80)

    def agachar(self):
        self.incUp.write(98)
        self.incDown.write(123)

    def inclinar(self):
        self.incUp.write(98)
        self.incDown.write(100)


class Controller:
    def __init__(self) -> None:
        self.brazo = Brazo()
        self.banda = Banda()

    def default(self):
        self.brazo.soltar()
        self.brazo.levantar()
        sleep(1)
        self.brazo.volver()
        sleep(1)
        self.brazo.cerrar()

    def agarrarCaja(self):
        self.brazo.soltar()
        sleep(1)
        self.brazo.volver()
        sleep(1)
        self.brazo.agachar()
        sleep(1)
        self.brazo.agarrar()
        sleep(1)

    def estacion(self,destino):
        self.brazo.levantar()
        sleep(1)
        self.brazo.mover(destino)
        sleep(1)
        self.brazo.inclinar()
        sleep(1)
        self.brazo.soltar()
        sleep(1)
        

def exit():
    board.exit()

board = pyfirmata.Arduino('COM7')  # Cambia el puerto según tu sistema


if __name__ == '__main__':
    controller = Controller()
    controller.banda.parar()
    controller.default()
    sleep(2)
    controller.agarrarCaja()
    sleep(2)
    controller.estacion(90)
    controller.default()
    sleep(2)
    controller.banda.mover()


    



    