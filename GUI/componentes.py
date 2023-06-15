from tkinter.ttk import Frame,Label,Spinbox,Treeview
from tkinter import Menu
from cv2 import cvtColor, COLOR_BGR2RGB, resize,INTER_AREA
from PIL import Image, ImageTk
from GUI.estilos.fuentes import TITLE_FONT
from data import set_data,get_data
from base.archivo import excel
from base import refresh,getAll

class BarMenu(Menu):
    def __init__(self,master,cursor):
        super().__init__(master)
        archivo_menu = Menu(self, tearoff= False)
        archivo_menu.add_separator()
        archivo_menu.add_command(
            label='Guardar',
            command=lambda: self.Guardar(cursor))
        archivo_menu.add_separator()
        self.add_cascade(menu=archivo_menu, label="Archivo")

    def Guardar(self,cursor):
        datos = getAll(cursor)
        excel(datos)

class Control(Frame):
    def __init__(self, master, text="label",_to=0,_increment=1,**kwargs):
        super().__init__(master, **kwargs)

        Label(master, text=text,justify="left",font=TITLE_FONT,style='Bar.TLabel').pack(in_=self,side="left",padx=10)

        self.spin = Spinbox(master)
        self.spin.config(from_=0, to=_to, increment=_increment, wrap=True)
        self.type = text.lower().replace(" ","_")
        datos=get_data()
        value = datos["deteccion"][self.type]
        self.spin.set(value)
        self.spin.bind('<ButtonRelease-1>', self.set_value)
        self.spin.pack(in_=self,side="right")
        

    def get_value(self):
        return self.spin.get()

    def set_value(self,e):
        datos = get_data()
        datos["deteccion"][self.type] = float(self.spin.get())

        set_data(datos)

class Camara(Frame):
    def __init__(self,master,title:str,tam:tuple[int,int],**kwargs):
        super().__init__(master,**kwargs)

        self.width,self.height = tam

        self.label = Label(self, text=title,font=TITLE_FONT)
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

class Img(Label):
    def __init__(self,master,file,width,height):
        super().__init__(master)
        img = Image.open(file)
        img = ImageTk.PhotoImage(img.resize((width,height),Image.LANCZOS))
        self.configure(image=img)
        self.image = img

class Tabla(Treeview):
    def __init__(self,master,cursor):
        self.cursor = cursor 
        super().__init__(master,columns=("0","1"),show='headings')
        #self.column("#0", width=0, minwidth=0)
        #self.heading("0", text="ID")
        self.heading("0", text="ID")
        self.heading("1", text="Destino")
        
        self.delete(*self.get_children())
        self.update()
        
    def update(self):
        self.delete(*self.get_children())
        rows = refresh(self.cursor)
        if not rows: return
        for row in rows:
            values = [value for value in row]
            self.insert("", "end", values=values)