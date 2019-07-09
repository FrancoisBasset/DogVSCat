import os
from tqdm import tqdm
import cv2
import numpy as np
from random import shuffle

TEST = "./Datasets/Test"
SIZE = 50

def process_test_data():
    testing_data = []
    img_num = 1

    for img in tqdm(os.listdir(TEST)):
        path = os.path.join(TEST, img)

        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (SIZE, SIZE))
        testing_data.append([np.array(img), img_num])

        img_num += 1

    return testing_data