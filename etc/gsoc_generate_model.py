import os
import subprocess
from itertools import product 
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

def run_bazel(model_name):
    proc = subprocess.Popen(
        ['sh', 'gsoc_proj/run.sh', './gsoc_proj/MODELS/{}'.format(model_name)],
        stdout = subprocess.PIPE
    )
    out, err = proc.communicate()
    latency_time = [float(i) for i in out.decode('utf-8').split('\n')[-11:-1]] # only gpu inference latency time..
    return sum(latency_time) / len(latency_time)


##################### MODEL GENERATION + RUN BENCHMARK #####################

"""
kernel_list = [2*i for i in range(10)]
filter_list = [2**i for i in range(4, 8)]
input_img_list = [(i, i, 3) for i in range(32, 512)]
"""
kernel_list = [1, 3, 5]
filter_list = [16, 32, 64]
input_hw = [8, 16, 32, 64]
input_channels = [16, 32, 48]
input_img_list = []
for hw in input_hw:
    for ch in input_channels:
        input_img_list.append((ch, hw, hw))


comb = list(product(kernel_list, filter_list, input_img_list)) # combination

data_frame = {
    'tflite_name' : [],
    'kernel' : [],
    'filter' : [],
    'input_shape' : [],
    'latency_time' : [],
}

for com in comb:
    _kernel, _filter, _input_shape = com
    model = keras.Sequential([
        keras.layers.Conv2D(filters=_filter, kernel_size=_kernel, input_shape=_input_shape, padding='same', activation='relu')
    ])
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    model_name = "kernel_{}_filter_{}_input_shape_{}.tflite".format(_kernel, _filter, _input_shape)
    with open("./MODELS/" + model_name, 'wb') as f:
        f.write(tflite_model)
    
    data_frame['tflite_name'].append(model_name)
    data_frame['kernel'].append(_kernel)
    data_frame['filter'].append(_filter)
    data_frame['input_shape'].append(_input_shape)
    # target value
    data_frame['latency_time'].append(run_bazel(model_name))

# save to csv
df = pd.DataFrame(data_frame)
df.to_csv('./resutl.csv')


