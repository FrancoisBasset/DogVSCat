import os
from tqdm import tqdm
import cv2
import numpy as np
from random import shuffle

CAT_TRAIN = "./Datasets/Cats/Images/"
DOG_TRAIN = "./Datasets/Dogs/images/"
SIZE = 50

training_data = []

for img in tqdm(os.listdir(CAT_TRAIN)):
    path = os.path.join(CAT_TRAIN, img)

    img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (SIZE, SIZE))
    training_data.append([np.array(img), np.array([1, 0])])


for folder in tqdm(os.listdir(DOG_TRAIN)):
    for img in tqdm(os.listdir(DOG_TRAIN + folder)):
        path = os.path.join(DOG_TRAIN, folder + "/" + img)

        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (SIZE, SIZE))
        training_data.append([np.array(img), np.array([0, 1])])


shuffle(training_data)
np.save("train_data.npy", training_data)