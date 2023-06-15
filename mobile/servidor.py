import socket
import pickle
import base
# Configuración del servidor
host = 'localhost'
port = 8000

# Crear un socket para el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a una dirección y puerto
server_socket.bind((host, port))

# Escuchar conexiones entrantes
server_socket.listen(1)

print('El servidor está esperando conexiones...')

""" # Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()
print('Se ha establecido una conexión desde:', client_address)
client_socket.send('conectado'.encode()) """

client_socket = None
client_address = None
enviado = False
message = pickle.dumps([1,2,3,4])

base.conexion()



# Recibir y enviar datos
while True:
    if client_socket is None: 
        client_socket, client_address = server_socket.accept()
        continue

    print('Se ha establecido una conexión desde:', client_address)
    data = client_socket.recv(1024).decode()
    print('Cliente:', data)
    if data=='adios':
        client_socket.close()
        client_socket = None


# Cerrar la conexión
client_socket.close()
server_socket.close()