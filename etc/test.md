
# GSOC Log, part 2

## 1. 가장 간단한 Conv2D 모델을 만들어봅시당

```python
import tensorflow as tf
from tensorflow import keras

model = keras.models.Sequential([
    keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=(112, 112, 3))
])
model.compile(optimizer='Adam'. loss='mean_squared_error')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('conv2d.tflite', 'wb') as f:
    f.write(tflite_model) 
```

