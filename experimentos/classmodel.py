import sets as gen



import tensorflow as tf
from os import path,mkdir

# cremaos nuestro modelo
if path.exists('modelo/modelo2.h5'): # si el modelo existe caragamos el modelo y sus pesos
    print('Cargando modelo...')
    modelo = tf.keras.models.load_model('modelo/modelo2.h5')
    modelo.load_weights('modelo/pesos2.h5')
    print("modelo cargado")
else: # de lo contrario lo creamos
    print('Creando modelo...')
    modelo = tf.keras.models.Sequential() # creamos el modelo secuenciol

    tam = 120

    # agregamos las capas
    modelo.add(tf.keras.layers.Convolution2D(5,(1,1),activation='relu', input_shape=(tam,tam,1))) # capa de convolucion
    modelo.add(tf.keras.layers.MaxPool2D((2,2))) # capa de maxpooling
    modelo.add(tf.keras.layers.Convolution2D(2,(10,10),activation='relu', input_shape=(tam,tam,1))) # capa de convolucion
    modelo.add(tf.keras.layers.Flatten()) # capa de aplanado
    modelo.add(tf.keras.layers.Dense(400, activation='relu')) # capa densa
    modelo.add(tf.keras.layers.Dense(4, activation='softmax')) # capa de salida

# compilamos el modelo
modelo.compile(loss='categorical_crossentropy', # funcion de perdida
                optimizer=tf.keras.optimizers.Adam(0.0001), # optimizador
                metrics=['accuracy', 'Precision']) # metricas de medicion
print("modelo creado")

# entrenamos el modelo
trainnings = 10
for i in range(trainnings):
    image_set,class_set = gen.getset()
    print(f'----dataset {i+1} de {trainnings}----')
    history = modelo.fit(
                        image_set,# dataset de entrenamiento
                        class_set,
                        epochs=4, # numero de epocas
                        batch_size=1
    )

if not path.exists('modelo'):
    mkdir('modelo')

# guardamos el modelo y sus pesos para su posterior uso
modelo.save('modelo/modelo2.h5')
modelo.save_weights('modelo/pesos2.h5')

if __name__=='__main__':
    print(history.history)
