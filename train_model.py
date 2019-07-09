import os
import numpy as np
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tflearn.datasets.mnist as mnist
import tensorflow

from test_data import process_test_data

SIZE = 50

tensorflow.reset_default_graph()

train_data = np.load("train_data.npy", allow_pickle=True)
test_data = process_test_data()

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

train = train_data[:-500]
test = train_data[-500:]


X = np.array([i[0] for i in train]).reshape(-1, SIZE, SIZE, 1)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1, SIZE, SIZE, 1)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), 
    snapshot_step=500, show_metric=True, run_id='dogvscat')

model.save("dogvscat")


import matplotlib.pyplot as plt

fig = plt.figure()

for num, data in enumerate(test_data):
    img_num = data[1]
    img_data = data[0]

    y = fig.add_subplot(3, 5, num + 1)

    orig = img_data
    data = img_data.reshape(SIZE, SIZE, 1)

    model_out = model.predict([data])[0]

    if np.argmax(model_out) == 1:
        str_label = "Dog"
    else:
        str_label = "Cat"

    y.imshow(orig, cmap="gray")
    plt.title(str_label)

    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)
plt.show()