import socket
import pickle


# Configuración del cliente
host = 'localhost'
port = 8000

# Crear un socket para el cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect((host, port))
print('Conexión establecida con el servidor.')

# Enviar y recibir datos
recive = False
while True:

    client_socket.send('quiero datos'.encode())
    data = client_socket.recv(4096)
    
    print('Servidor:', pickle.loads(data))


# Cerrar la conexión
client_socket.close()