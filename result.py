from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
import matplotlib.pyplot as plt
import tflearn
import os
import numpy as np
from test_data import process_test_data
from test_data import process_test_data_debug
import sys

debug = len(sys.argv) == 1

if debug == True:
    test_data = process_test_data_debug()
else:
    test_data = process_test_data(sys.argv[1])

#debug = True

fig = plt.figure()

SIZE = 50

convnet = input_data(shape=[None, SIZE, SIZE, 1], name='input')

convnet = conv_2d(convnet, 32, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 32, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 32, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=1e-20, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

if os.path.exists("dogvscat.meta"):
    model.load("dogvscat")
    print("model loaded")

for num, data in enumerate(test_data):
    img_num = data[1]
    img_data = data[0]

    orig = img_data
    data = img_data.reshape(SIZE, SIZE, 1)

    model_out = model.predict([data])[0]

    if np.argmax(model_out) == 1:
        str_label = "Dog"
    else:
        str_label = "Cat"
    
    print(str_label, end="")

    if debug == True:
        y = fig.add_subplot(3, 5, num + 1)

        y.imshow(orig, cmap="gray")
        plt.title(str_label)

        y.axes.get_xaxis().set_visible(False)
        y.axes.get_yaxis().set_visible(False)

if debug == True:
    plt.show()