import os
from tqdm import tqdm
import cv2
import numpy as np
from random import shuffle

SIZE = 50

def process_test_data_debug():
    DIR = "./Datasets/Test"
    testing_data = []
    img_num = 1

    for img in tqdm(os.listdir(DIR)):
        path = os.path.join(DIR, img)

        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (SIZE, SIZE))
        testing_data.append([np.array(img), img_num])

        img_num += 1

    return testing_data

def process_test_data(filename):
    testing_data = []

    img = cv2.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), (SIZE, SIZE))
    testing_data.append([np.array(img), 1])

    return testing_data