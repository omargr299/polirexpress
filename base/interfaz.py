import tkinter as tk
import tkinter.ttk as ttk
import base
import colores as col

class App(tk.Tk):
    def __init__(self,conex) -> None:
        super().__init__()

        self.conex = conex

        self.title('poliexpress')
        self.geometry('600x300')
        
        self.container =tk.Frame(self,background=col.delantero,relief='solid')
        self.container.pack(expand=True,fill='both')

        self.tabla = Tabla(self.container, self.conex.cursor())
        self.tabla.pack(expand=True,fill='both')

        self.bar=tk.Frame(self,background=col.delantero,relief='solid')
        self.bar.pack(fil='x',before=self.tabla )

        self.titulo= tk.Label(self.bar,text="POLIEXPRESS",
                               background=col.delantero, foreground='white'
                               ,font=("Eras Bolt ITC" ,33))
        self.titulo.pack(pady=20)
        self.mainloop()

def tabla_de_datos():
    inter = App(base.conexion('poliexpress','poliexpress'))
    inter.mainloop()
         
    inter.tabla.update()
    inter.mainloop()

class Tabla(ttk.Treeview):
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
        rows = base.refresh(self.cursor)
        if not rows: return
        for row in rows:
            values = [value for value in row]
            self.insert("", "end", values=values)



if __name__=="__main__":
    App(base.conexion('poliexpress','poliexpress'))