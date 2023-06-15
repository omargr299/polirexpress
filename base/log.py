from tkinter import Tk,StringVar
from tkinter.ttk import Label,Entry,Button,Frame,Style
from GUI.estilos.colores import *
from GUI.estilos.fuentes import *
import base 

class LogIn(Tk):
    def __init__(self):
        super().__init__()

        self.destroyed = False

        self.title('PoliExpress')
        self.geometry('500x300')
        self.resizable(False,False)
        self.iconbitmap("./resources/logo.ico")
        self.configure(background=BASE)

        style = Style()
        style.theme_use('alt')
        
        style.configure("TEntry", fieldbackground=BASE,foreground=FORE,font=ENTRY_FONT)
        style.configure("TButton", background=MAIN,foreground=MAIN_FORE,font=ENTRY_FONT)
        style.map("TButton", 
                    background=[
                      ('pressed','!disabled',HIGH),
                      ('active', '!disabled', MAIN)],
                    foreground=[('active', '!disabled', FORE)])
        style.configure("Bar.TFrame", background=MAIN)
        style.configure("Container.TFrame", background=BASE)
        style.configure("TLabel", background=BASE,foreground=FORE,font=NORMAL_FONT)

        self.bar= Frame(self,style="Bar.TFrame")
        self.bar.pack(side='top',fil='x')

        Label(self.bar,text="POLIEXPRESS",
                           foreground=MAIN_FORE,
                               background=MAIN
                               ,font=LOGO_FONT).pack(pady=10)
        
        self.warning= Label(self,foreground="red")
        self.warning.pack(pady=10)

        
        self.container =Frame(self,style="Container.TFrame")
        self.container.pack(expand=True)

        Label(self.container,text="Usuario:").grid(column=0,row=0,padx=5,pady=10)

        Label(self.container,text="Contraseña:").grid(column=0,row=1,padx=5,pady=10)

        self.usuario_dato= StringVar()
        self.usuario_contra= StringVar()

        self.usuario = Entry(self.container,width=20, textvariable=self.usuario_dato,
                                )
        self.usuario.grid(column=1,row=0,padx=5,pady=10)

        self.contra = Entry(
            self.container,
            width=20,
            textvariable=self.usuario_contra,
            show="•" 
        )
        self.contra.grid(column=1,row=1,padx=5,pady=10)


        self.boton= Button(self, text="Entrar",
                                      cursor="hand2",
                                     command=self.conectar)
        self.boton.pack(side='bottom',pady=20)

        self.loop = True
        self.conex = None

        #cuando la ventana se destruye se interrupe el ciclo
        self.bind("<Destroy>", lambda e: self.interrrumpir())

    def interrrumpir(self): 
        self.loop=False
        self.destroyed = True

    def bucle(self):
        while self.loop:
            self.update()

        if not self.destroyed: self.destroy()
        return self.conex

    def conectar(self):
        usu = str(self.usuario_dato.get())
        cont = str(self.usuario_contra.get())
        self.conex = base.conexion(usu,cont)
        if self.conex is None:
            self.warning.configure(text="intenta de nuevo")
        else:
            self.loop = False


if __name__=='__main__':
    app = LogIn()
    app.mainloop()
