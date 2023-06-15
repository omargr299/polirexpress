from tkinter.ttk import Frame,Label,Button

from GUI.estilos.colores import *
from GUI.estilos.fuentes import TITLE_FONT,TYPE_FONT

from GUI.componentes import Img,Camara,Control

class Bar(Frame):
    def __init__(self,master):
        super().__init__(master,style="Bar.TFrame")
        img_tam = 60
        self.logo = Img(self,"./resources/logo.png",img_tam,img_tam)
        self.logo.pack(side="left",padx=5,pady=5)
        self.logo.configure(style="Logo.TLabel")



class Controles(Frame):
    def __init__(self,master):
        super().__init__(master,style="Bar.TFrame")
        self.area = Control(self,"Area",100000,1000,style="Bar.TFrame")
        self.lados = Control(self,"Lados",10,1,style="Bar.TFrame")
        self.aspect = Control(self,"Aspect ratio",10,0.1,style="Bar.TFrame")
        self.area.grid(row=0,column=0)
        self.lados.grid(row=0,column=1)
        self.aspect.grid(row=0,column=2)




class Camaras(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.content = Frame(self)
        ra = 9/16
        camwidht = 600
        camheight = int(camwidht*ra)
        self.imagen = Camara(self.content,"Camara",(camwidht,camheight))   
        self.contornos= Camara(self.content,"Contornos",((camwidht//2),(camheight//2)))
        self.etiqueta = Camara(self.content,"Etiqueta",((camheight//3),(camheight//3)))
        Label(self.etiqueta,text="Tipo:",font=TITLE_FONT).pack()
        self.label_etiqueta = Label(self.etiqueta,text="N/A",font=TYPE_FONT)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.content.grid(column=0,row=0)
        self.imagen.grid(row=0,column=0,rowspan=2)
        self.contornos.grid(row=0,column=1)
        self.etiqueta.grid(row=1,column=1)
        self.label_etiqueta.pack()



class Botones(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.continuar = Button(self,text="Continuar")
        self.continuar.pack(side='left',padx=5,pady=5)
        self.parar = Button(self,text="Parar")
        self.parar.pack(side='left',padx=5,pady=10)