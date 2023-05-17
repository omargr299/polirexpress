import tkinter as tk
import colores as col
import base
import interfaz

class LogIn(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas1=tk.Canvas(self, width=600, height=400, background=col.trasero)
        self.canvas1.create_rectangle(0,0, 600,70, fill=col.delantero)
        self.canvas1.grid(row=0, column=0, sticky="ew")

        self.titulo= tk.Label(self,text="POLIEXPRESS",
                               background=col.delantero, foreground='white'
                               ,font=("Eras Bolt ITC" ,33))
        self.titulo.place(x=170,y=6)

        self.usuario= tk.Label(self,text="Usuario:",
                               background=col.trasero, foreground='white'
                               ,font=("Roboto" ,12))
        self.usuario.place(x=216,y=200)
        self.contraseña= tk.Label(self,text="Contraseña:",
                               background=col.trasero, foreground='white'
                               ,font=("Roboto" ,12))
        self.contraseña.place(x=216,y=270)

        self.usuario_dato= tk.StringVar()
        self.usuario_contra= tk.StringVar()

        self.usuario_entrada = tk.Entry(self,width=20, textvariable=self.usuario_dato, 
                                foreground="white", background=col.entradas
                                ,font=("Verdana" ,12))
        self.usuario_entrada.place(x=216,y=220)

        self.contra_entrada = tk.Entry(
            width=20,
            textvariable=self.usuario_contra,
            foreground="white",
            background=col.entradas,
            font=("Verdana", 12),
            show="•" 
        )

        self.contra_entrada.place(x=216,y=290)

        self.boton_entrada=tk.Button(self, text="Entrar",
                                     background=col.delantero, foreground='white'
                                     ,font=("Verdana" ,13)
                                     , command=self.entrar)
        self.boton_entrada.place(x=286,y=340)

    def entrar(self):
        usu = str(self.usuario_dato.get())
        cont = str(self.usuario_contra.get())
        conex = base.conexion(usu,cont)
        if base.conexion is None:
            self.warning= tk.Label(text="intenta de nuevo")
            self.warning.place(x=170,y=6)
        else:
            inter = interfaz.App(conex)
            inter.mainloop()

app = LogIn()
app.mainloop()
