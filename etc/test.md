
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

여기까지는 성공! 

## 2. Conv2D의 파라미터를 알아보자.

Convolution 2D에는 여러가지 파라미터가 있는데, 쉽게 알 수 있는 것을 알아보자면

- padding size (HxW)
- input/output tensor size
- stride (HxW)
- kernel size (HxW)
- dilation size (HxW)

이것들을 어떻게 알 수 있을까! 알아봐야겠당.

