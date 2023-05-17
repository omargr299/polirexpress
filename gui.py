import tkinter as tk
from tkinter import ttk
import data
from PIL import Image, ImageTk
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, CAP_DSHOW, resize,INTER_AREA,imshow

from pygrabber.dshow_graph import FilterGraph

NORMAL_FONT = ('Roboto', 13)
TITLE_FONT = ('Roboto', 13,'italic')
TYPE_FONT = ('Roboto', 13, 'bold')



class GUI(tk.Tk):
    def __init__(self,title,resizable=False,exit=lambda e: print("Goodbye")):
        super().__init__()
        self.title(title)
        self.resizable(resizable, resizable)
        self.bind("<Destroy>", exit)

        self.cams = FilterGraph().get_input_devices()
        self.config = data.get_data()

        self.create_widgets()

        self.cam = VideoCapture(self.select_cam.current(),CAP_DSHOW)

        style = ttk.Style()
        style.configure("TEntry", font=NORMAL_FONT)
        style.configure("TLabel", background="#ffffff",font=NORMAL_FONT)
        style.configure("TFrame", background="#ffffff")
        style.configure("Bar.TLabel", background="#6b1740",foreground="#ffffff")
        style.configure("Bar.TFrame", background="#6b1740")
        style.configure("Logo.TLabel", background="#6b1740")
        style.configure('TCombobox',fieldbackground= "orange",background= "red")
        
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        self.minsize(width,height)

    def create_widgets(self):
        #main panel
        self.main = ttk.Frame(self,style="Main.TFrame")
        #layout
        self.main.pack(expand=True,fill='both')

        img_tam = 60
        self.bar = ttk.Frame(self.main,style="Bar.TFrame")
        self.bar.pack(side="top",fill="x")
        self.logo = Img(self.bar,"resources/logo.png",img_tam,img_tam)
        self.logo.configure(style="Logo.TLabel")
        self.logo.pack(side="left",padx=5,pady=5)

        #----------------------------

        #control panel
        self.panel_control = ttk.Frame(self.bar,style="Bar.TFrame")
        self.area = Control(self.panel_control,"Area",100000,1000,style="Bar.TFrame")
        self.lados = Control(self.panel_control,"Lados",10,1,style="Bar.TFrame")
        self.aspect = Control(self.panel_control,"Aspect ratio",10,0.1,style="Bar.TFrame")
        #layout
        self.area.grid(row=0,column=0)
        self.lados.grid(row=0,column=1)
        self.aspect.grid(row=0,column=2)
        self.panel_control.pack(side='right',pady=20,padx=20)

        #----------------------------

        #select control
        self.select_panel = ttk.Frame(self.main)
        ttk.Label(self.select_panel,text="Seleccione la camara",font=TITLE_FONT).pack(side="left",padx=5)
        self.select_cam = ttk.Combobox(self.select_panel,values=self.cams,state="readonly")
        #info
        cam = self.config["camara"]
        cam = cam if cam!="None" else self.cams[0]
        cam = cam if cam in self.cams else "None"
        self.config["camara"] = cam
        data.set_data(self.config)
        self.select_cam.set(cam)
        #bindings
        self.select_cam.bind("<<ComboboxSelected>>", self.set_cam)
        #layout
        self.select_cam.pack(side="left",padx=5)
        self.select_panel.pack(pady=20)

        #----------------------------
        
        #panel camaras
        self.panel_camaras = ttk.Frame(self.main) 
        self.content = ttk.Frame(self.panel_camaras)
        ra = 9/16
        camwidht = 600
        camheight = int(camwidht*ra)
        self.imagen = Camara(self.content,"Camara",(camwidht,camheight))   
        self.contornos= Camara(self.content,"Contornos",((camwidht//2),(camheight//2)))
        self.etiqueta = Camara(self.content,"Etiqueta",((camheight//3),(camheight//3)))
        ttk.Label(self.etiqueta,text="Tipo:",font=TITLE_FONT).pack()
        self.label_etiqueta = ttk.Label(self.etiqueta,text="N/A",font=TYPE_FONT)

        #layout
        self.panel_camaras.pack(pady=20,expand=True,fill="both")
        self.content.pack()
        self.imagen.grid(row=0,column=0,rowspan=2)
        self.contornos.grid(row=0,column=1)
        self.etiqueta.grid(row=1,column=1)
        self.label_etiqueta.pack()

        self.wcam = self.panel_camaras.winfo_width()
        self.hcam = self.panel_camaras.winfo_height()
        self.panel_camaras.bind("<Configure>",self.change_size)

        self.botones = ttk.Frame(self)
        self.botones.pack(side="bottom",fill="x")
        self.continuar = ttk.Button(self.botones,text="Continuar")
        self.continuar.pack(side='left',padx=5,pady=5)
        self.parar = ttk.Button(self.botones,text="Parar")
        self.parar.pack(side='left',padx=5,pady=5)

    def update_window(self):
        self.update()
        self.update_idletasks()

    def set_cam(self,e):
        seleccion = self.select_cam.current()
        self.config["camara"] = self.select_cam["values"][seleccion]
        data.set_data(self.config)
        self.cam = VideoCapture(seleccion,CAP_DSHOW)

    def update_cams(self):
        self.cams = FilterGraph().get_input_devices()
        self.select_cam.config(values=self.cams)
    
    def update_screen(self,frame):
        self.imagen.update_frame(frame)

    def get_frame(self):
        return self.cam.read()
    
    def update_contornos(self,frame):
        self.contornos.update_frame(frame)
    
    def update_etiqueta(self,frame):
        self.etiqueta.update_frame(frame)

    def set_etiqueta(self,text):
        self.label_etiqueta.configure(text=text)
    
    def default_cams(self):
        #self.imagen.set_default()
        self.contornos.set_default()
        self.etiqueta.set_default()
        self.label_etiqueta.configure(text="N/A")

    def change_size(self,e):
        war,har=e.width/self.wcam,e.height/self.hcam
        self.wcam = e.width
        self.hcam = e.height
        if war>10 or har>10: return
        self.imagen.change_size(war,har)
        self.contornos.change_size(war,har)
        self.etiqueta.change_size(war,har)
        self.imagen.set_image(self.imagen.screen.image)
        self.contornos.set_image(self.contornos.screen.image)
        self.etiqueta.set_image(self.etiqueta.screen.image) 
    
class Panel(ttk.Frame):
    def __init__(self, master,**kwargs):
        super().__init__(master, **kwargs)
        self.children_ = []
        self.pack(pady=5)
        

    def add_child(self, child):
        child.pack(in_=self, side="top", pady=2)
        self.children_.append(child)        
        self.pack()


class Control(ttk.Frame):
    def __init__(self, master, text="label",_to=0,_increment=1,**kwargs):
        super().__init__(master, **kwargs)

        ttk.Label(master, text=text,justify="left",font=TITLE_FONT,style='Bar.TLabel').pack(in_=self,side="left",padx=10)

        self.spin = ttk.Spinbox(master)
        self.spin.config(from_=0, to=_to, increment=_increment, wrap=True)
        self.type = text.lower().replace(" ","_")
        datos=data.get_data()
        value = datos["deteccion"][self.type]
        self.spin.set(value)
        self.spin.bind('<ButtonRelease-1>', self.set_value)
        self.spin.pack(in_=self,side="right")
        

    def get_value(self):
        return self.spin.get()

    def set_value(self,e):
        datos = data.get_data()
        datos["deteccion"][self.type] = float(self.spin.get())

        data.set_data(datos)
        
    
class Camara(ttk.Frame):
    def __init__(self,master:tk.Tk,title:str,tam:tuple[int,int],**kwargs):
        super().__init__(master,**kwargs)

        self.width,self.height = tam

        self.label = ttk.Label(self, text=title,font=TITLE_FONT)
        self.label.pack()

        self.screen = Img(self,'resources/no_cam.jpg',self.width,self.height)
        self.default = self.screen.image
        self.screen.pack()

    def update_frame(self,frame):
        frame = cvtColor(frame, COLOR_BGR2RGB)
        frame = resize(frame,(self.width,self.height),interpolation=INTER_AREA)
        img = Image.fromarray(frame)
        self.set_image(ImageTk.PhotoImage(img))

    def set_default(self):
        self.set_image(self.default)

    def set_image(self,imagen):
        self.screen.configure(image=imagen)
        self.screen.image = imagen

    def change_size(self,war,har):
        self.width *= war
        self.height *= har
        self.width = int(self.width)
        self.height = int(self.height)


class Img(ttk.Label):
    def __init__(self,master,file,width,height):
        super().__init__(master)
        img = Image.open(file)
        img = ImageTk.PhotoImage(img.resize((width,height),Image.LANCZOS))
        self.configure(image=img)
        self.image = img

if __name__ == "__main__":
    loop = True

    def exit(e):
        global loop
        loop = False

    wnd = GUI("Test", exit=exit, resizable=True)

    while loop:
        rect,frame = wnd.cam.read()
        if rect:
            wnd.imagen.update_frame(frame)
        else:
            wnd.imagen.set_default()
        wnd.update_cams()
        wnd.update_window()