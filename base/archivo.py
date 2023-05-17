import tkinter as tk
import interfaz
import base
import openpyxl as xl

def iniciar():
    pagina = tk.Tk()
    archivo = tk.Menu(pagina)
    archivo_menu = tk.Menu(archivo, tearoff= False)
    archivo_menu.add_command(
        label='Tabla de datos',
        command=tabla_de_datos)
    archivo_menu.add_command(
        label='Guardar',
        command=excel)
    archivo.add_cascade(menu=archivo_menu, label="Archivo")
    pagina.config(menu=archivo)
    pagina.mainloop()

def tabla_de_datos():
    inter = interfaz.App(base.conexion('poliexpress','poliexpress'))
    inter.mainloop()

def excel(datos:list):
    wb = xl.Workbook()
    sheet = wb.active
    if sheet is None: return
    sheet.cell(row=1,column=1,value='ID')
    sheet.cell(row=1,column=2,value='Destino')
    sheet.cell(row=1,column=3,value='Fecha')
    for indice,registro in enumerate(datos):
        sheet.cell(row=indice+2,column=1,value=registro[0])
        sheet.cell(row=indice+2,column=2,value=registro[1])
        sheet.cell(row=indice+2,column=3,value=registro[2].strftime('%d/%m/%Y %H:%M:%S'))

    wb.save('registros.xlsx')

if __name__=='__main__':

    iniciar()


    