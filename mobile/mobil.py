
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import socket
import pickle

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        button = Button(text='Haz clic', on_release=self.on_button_click,size_hint=(None, None), size=(200, 200))
        layout.add_widget(button)

        self.tableheight = 100
        self.table_layout = BoxLayout(orientation='vertical',size_hint=(None,None),size=(500,self.tableheight))
        
        # Crear la fila de encabezados
        header_layout = BoxLayout(orientation='horizontal',size_hint=(None,None),size=(500,100))
        header_layout.add_widget(Label(text='Encabezado 1'))
        header_layout.add_widget(Label(text='Encabezado 2'))
        header_layout.add_widget(Label(text='Encabezado 3'))
        self.table_layout.add_widget(header_layout)
        layout.add_widget(self.table_layout)



        """ host = 'localhost'
        port = 8000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print('Conexión establecida con el servidor.')
 """
        
        return layout
    
    def on_button_click(self, instance):
        instance.text = '¡Haz clic de nuevo!'
        header_layout = BoxLayout(orientation='horizontal',size_hint=(None,None),size=(500,100))
        header_layout.add_widget(Label(text='0'))
        header_layout.add_widget(Label(text='1'))
        header_layout.add_widget(Label(text='2'))
        self.tableheight += 100
        self.table_layout.size = (500,self.tableheight)
        self.table_layout.add_widget(header_layout)
        #self.client_socket.send('quiero datos'.encode())

    def on_stop(self):
        # Acciones a realizar cuando la ventana se cierra
        #self.client_socket.send('adios'.encode())
        #self.client_socket.close()
        print("La ventana se ha cerrado")

    def run(self):
        print("La aplicación se está ejecutando")
        #Clock.schedule_interval(self.custom_update, 1.0)  # Llama a custom_update cada segundo
        super(MyApp, self).run()
        print("La aplicación se ha cerrado")
        
if __name__ == '__main__':
    MyApp().run()