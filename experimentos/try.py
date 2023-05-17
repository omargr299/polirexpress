
import tensorflow as tf
from os import path,mkdir

inputs = tf.keras.layers.Input(shape=(1,))
l1 = tf.keras.layers.Dense(3)(inputs)
outputs1  = tf.keras.layers.Dense(1)(l1)
outputs2 = tf.keras.layers.Dense(2)(l1)

modelo = tf.keras.models.Model(inputs=[inputs],outputs=[outputs1,outputs2]  )


# compilamos el modelo
modelo.compile(loss=[tf.keras.losses.mean_squared_error,tf.keras.losses.mean_absolute_error], # funcion de perdida
                optimizer=tf.keras.optimizers.Adam(0.01), # optimizador
                metrics=['accuracy', 'Precision']) # metricas de medicion
print("modelo creado")

x = tf.constant([[1]])
y1 = tf.constant([[1,2]])
y2 = tf.constant([[1]])
modelo.fit(
    x,
    (y2,y1),
)

print(modelo.predict(x))
