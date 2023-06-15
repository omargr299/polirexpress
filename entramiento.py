import generador as gen
from data import get_data


import tensorflow as tf
from os import path,mkdir

model_name = 'modelo/modelo-1.h5'
pesos_name = 'modelo/pesos-1.h5'
# cremaos nuestro modelo
if path.exists(model_name): # si el modelo existe caragamos el modelo y sus pesos
    print('Cargando modelo...')
    modelo = tf.keras.models.load_model(model_name)
    modelo.load_weights(pesos_name)
    print("modelo cargado")
else: # de lo contrario lo creamos
    print('Creando modelo...')
    modelo = tf.keras.models.Sequential() # creamos el modelo secuenciol

    tam = get_data()["image"]

    # agregamos las capas
    modelo.add(tf.keras.layers.Convolution2D(10,(3,3),activation='relu', input_shape=(tam,tam,1))) # capa de convolucion
    modelo.add(tf.keras.layers.MaxPool2D((2,2))) # capa de maxpooling
    modelo.add(tf.keras.layers.Convolution2D(5,(20,20),activation='relu', input_shape=(tam,tam,1))) # capa de convolucion


    modelo.add(tf.keras.layers.Flatten()) # capa de aplanado
    modelo.add(tf.keras.layers.Dense(400, activation='relu')) # capa densa
    modelo.add(tf.keras.layers.Dense(4, activation='softmax')) # capa de salida

# compilamos el modelo
modelo.compile(loss='categorical_crossentropy', # funcion de perdida
                optimizer=tf.keras.optimizers.Adam(0.000001), # optimizador
                metrics=['accuracy', 'Precision']) # metricas de medicion
print("modelo creado")
    

# entrenamos el modelo
trainnings = 20
for i in range(trainnings):
    print(f'----dataset {i+1} de {trainnings}----')
    # creamoos el dataset de etiquetas deformadas
    x,y = gen.generateReal()
    history = modelo.fit(
                        x,# dataset de entrenamiento
                        y,
                        epochs=8, # numero de epocas
                        batch_size=4, # tamaño del batch
)

if not path.exists('modelo'):
    mkdir('modelo')

# guardamos el modelo y sus pesos para su posterior uso
modelo.save(model_name)
modelo.save_weights(pesos_name)

if __name__=='__main__':
    print(history.history)
