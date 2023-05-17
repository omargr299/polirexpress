


import tensorflow as tf
from os import path,mkdir

m_name = 'modelo/modelo3-4.h5'
w_name = 'modelo/pesos3-4.h5'
# cremaos nuestro modelo
if path.exists(m_name): # si el modelo existe caragamos el modelo y sus pesos
    print('Cargando modelo...')
    modelo = tf.keras.models.load_model(m_name)
    modelo.load_weights(w_name)
    print("modelo cargado")
else: # de lo contrario lo creamos
    print('Creando modelo...')
    modelo = tf.keras.models.Sequential() # creamos el modelo secuenciol

    tam = 40

    # agregamos las capas
    modelo.add(tf.keras.layers.Convolution2D(10,(1,1),activation='relu', input_shape=(tam,tam,1))) # capa de convolucion
    modelo.add(tf.keras.layers.Convolution2D(5,(3,3),activation='relu' )) # capa de convolucion
    modelo.add(tf.keras.layers.Convolution2D(2,(1,1),activation='relu' )) # capa de convolucion
    modelo.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2))) # capa de maxpooling
    modelo.add(tf.keras.layers.Flatten()) # capa de aplanado
    modelo.add(tf.keras.layers.Dense(400, activation='relu')) # capa densa
    modelo.add(tf.keras.layers.Dense(25, activation='sigmoid')) # capa densa

# compilamos el modelo
modelo.compile(loss=tf.keras.losses.binary_crossentropy, # funcion de perdida
            optimizer=tf.keras.optimizers.Adam(0.000001), # optimizador
            metrics=[tf.keras.metrics.binary_accuracy, tf.keras.metrics.Precision()]) # metricas de medicion
print("modelo creado")

# entrenamos el modelo
import sets as gen
trainnings = 10
for i in range(trainnings):
    image_set,series_set = gen.getset2()
    print(f'----dataset {i+1} de {trainnings}----')

    history = modelo.fit(
                        image_set,# dataset de entrenamiento
                       series_set,
                        epochs=4, # numero de epocas
                        batch_size=1
    )

if not path.exists('modelo'):
    mkdir('modelo')

# guardamos el modelo y sus pesos para su posterior uso
modelo.save(m_name)
modelo.save_weights(w_name)
