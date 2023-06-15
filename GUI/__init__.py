from tkinter import Tk
from tkinter.ttk import Style,Frame,Combobox,Label
import data
from cv2 import VideoCapture, CAP_DSHOW
from base import log
from GUI.componentes import Tabla
from GUI.componentes import BarMenu
from GUI.estilos.colores import *
from GUI.estilos.fuentes import *
import GUI.paneles as paneles

from pygrabber.dshow_graph import FilterGraph

class App(Tk):
    def __init__(self,title,resizable=False,finish=lambda e: print("Goodbye")):
        
        print("Iniciando...")
        self.conex = log.LogIn().bucle()
        if self.conex is None: exit()
        print("loggin exitoso")
        super().__init__()

        style = Style()
        style.theme_use('clam')
     

        self.title(title)
        self.resizable(resizable, resizable)
        self.menu=BarMenu(self,self.conex.cursor())
        self.config(menu=self.menu)
        self.iconbitmap("./resources/logo.ico")
        self.bind("<Destroy>", finish)


        self.cams = FilterGraph().get_input_devices()
        self.config = data.get_data()

        self.create_widgets()

        self.cam = VideoCapture(self.select_cam.current(),CAP_DSHOW)

        style.configure("TEntry", font=NORMAL_FONT)
        style.configure("TLabel", background="#ffffff",font=NORMAL_FONT)
        style.configure("TFrame", background="#ffffff")
        style.configure("Bar.TLabel", background="#6b1740",foreground="#ffffff")
        style.configure("Bar.TFrame", background="#6b1740")
        style.configure("Logo.TLabel", background="#6b1740")
        style.configure("TButton", background=MAIN,foreground="white",font=("Roboto" ,12),relief="raised",justify='center')
        style.map("TButton", 
            background=[
                ('pressed','!disabled',HIGH),
                ('active', '!disabled', MAIN)],
            foreground=[('active', '!disabled', 'white')])
        style.configure('Treeview.Heading', background=MAIN,foreground=MAIN_FORE,font=TITLE_FONT)
        style.configure('TCombobox',
                        arrowcolor=MAIN,
                        fieldbackground=BASE,
                        foreground=FORE,
                        font=TITLE_FONT,
                        selectbackground=BASE,
                        selectforeground=FORE,
                        insertbackground=BASE)
        style.map('TCombobox', fieldbackground=[('readonly', 'white')],foreground=[('readonly', 'black')])
        style.configure('TSpinbox',arrorcolor=MAIN,fieldbackground=BASE,foreground=FORE,font=TITLE_FONT)
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        self.minsize(width,height)

    def create_widgets(self):
        #main panel
        self.main = Frame(self,style="Main.TFrame")
        #layout
        self.main.pack(expand=True,fill='both')

        #----------------------------

        #barra superior
        img_tam = 60
        self.bar = paneles.Bar(self.main)
        self.bar.pack(side="top",fill="x")

        #----------------------------

        #control panel
        self.panel_control = paneles.Controles(self.bar)
        self.panel_control.pack(side='right',pady=20,padx=20)

        #----------------------------

        #select control
        self.select_panel = Frame(self.main)
        Label(self.select_panel,text="Seleccione la camara",font=TITLE_FONT).pack(side="left",padx=5)
        self.select_cam = Combobox(self.select_panel,values=self.cams,state="readonly",style="TCombobox")
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
        self.camaras = paneles.Camaras(self.main)
        self.camaras.pack(pady=20,padx=20,fill="both",expand=True)

        self.wcam = self.camaras.winfo_width()
        self.hcam = self.camaras.winfo_height()
        self.camaras.bind("<Configure>",self.change_size)
        
        #----------------------------

        #tabla
        self.tabla = Tabla(self.camaras,self.conex.cursor())
        self.tabla.grid(column=1,row=0,sticky="nswe",padx=20) 

        #----------------------------

        #botones
        self.botones = paneles.Botones(self)
        self.botones.pack(side="bottom",fill="x",padx=20)
        

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
        self.camaras.imagen.update_frame(frame)

    def get_frame(self):
        return self.cam.read()
    
    def update_contornos(self,frame):
        self.camaras.contornos.update_frame(frame)
    
    def update_etiqueta(self,frame):
        self.camaras.etiqueta.update_frame(frame)

    def set_etiqueta(self,text):
        self.camaras.label_etiqueta.configure(text=text)
    
    def default_cams(self):
        #self.imagen.set_default()
        self.camaras.contornos.set_default()
        self.camaras.etiqueta.set_default()
        self.camaras.label_etiqueta.configure(text="N/A")

    def change_size(self,e):
        war,har=e.width/self.wcam,e.height/self.hcam
        self.wcam = e.width
        self.hcam = e.height
        if war>10 or har>10: return
        self.camaras.imagen.change_size(war,har)
        self.camaras.contornos.change_size(war,har)
        self.camaras.etiqueta.change_size(war,har)
        self.camaras.imagen.set_image(self.camaras.imagen.screen.image)
        self.camaras.contornos.set_image(self.camaras.contornos.screen.image)
        self.camaras.etiqueta.set_image(self.camaras.etiqueta.screen.image) 


if __name__ == "__main__":
    loop = True

    def finish(e):
        global loop
        loop = False

    wnd = App("Test", finish=finish, resizable=True)

    while loop:
        rect,frame = wnd.cam.read()
        if rect:
            wnd.imagen.update_frame(frame)
        else:
            wnd.imagen.set_default()
        wnd.update_cams()
        wnd.update_window()


