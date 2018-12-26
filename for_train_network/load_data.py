import numpy as np
import os
from sklearn.utils import shuffle

def load_data():
    # print(os.getcwd())
    PATH = os.getcwd()
    data_path = PATH + '/data'
    for files in os.listdir(data_path):
        print(files)
        file_name = files.split('.')
        name = file_name[0].split('_')
        print("\t", name[4])
        loaded = np.load(data_path + '/' + files)
        if name[4] == 'Labels':
            labels = loaded
            print("DONE", loaded.shape)
        elif name[4] == 'Images':
            images = loaded
            print("DONE", loaded.shape)

    print("Images sizes ", np.shape(images))
    print("Labels sizes ", np.shape(labels))

    x, y = shuffle(images, labels, random_state=2)
    return x, y
