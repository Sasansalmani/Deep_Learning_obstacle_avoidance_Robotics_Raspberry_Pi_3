import sys
import numpy as np
import os
import cv2

def switch_demo(argument):
    switcher = {
        1: [1,0,0,0,0,0,0,0],
        2: [0,1,0,0,0,0,0,0],
        3: [0,0,1,0,0,0,0,0],
        4: [0,0,0,1,0,0,0,0],
        5: [0,0,0,0,1,0,0,0],
        6: [0,0,0,0,0,1,0,0],
        7: [0,0,0,0,0,0,1,0],
        8: [0,0,0,0,0,0,0,1],
    }
    return switcher.get(argument)

def load_images_from_folder(folder, numbers, labels, images, label):
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        img = cv2.resize(img, (224, 224))
        #print(filename)
        #for part in filename.split("."):
        #    print("------------"+part)
        cv2.imshow("image is loading", img)
        cv2.waitKey(10)
        numbers+=1
        if img is not None:
            images.append(np.asarray(img))
            labels.append(np.asarray(label))
    print("\t\tDONE\n\t{} images loaded".format(numbers))
    return numbers, labels, images

def folders_in_main_folder(folder, save_name):
    images = []
    labels = []
    numbers = 0
    numbers, labels, images = load_images_from_folder(folder+"\\back", numbers, labels, images, switch_demo(1))
    numbers, labels, images = load_images_from_folder(folder+"\\f_left", numbers, labels, images, switch_demo(2))
    numbers, labels, images = load_images_from_folder(folder+"\\f_right", numbers, labels, images, switch_demo(3))
    numbers, labels, images = load_images_from_folder(folder+"\\front", numbers, labels, images, switch_demo(4))
    numbers, labels, images = load_images_from_folder(folder+"\\left", numbers, labels, images, switch_demo(5))
    numbers, labels, images = load_images_from_folder(folder+"\\right", numbers, labels, images, switch_demo(6))
    numbers, labels, images = load_images_from_folder(folder+"\\t_left", numbers, labels, images, switch_demo(7))
    numbers, labels, images = load_images_from_folder(folder+"\\t_right", numbers, labels, images, switch_demo(8))
    np.save(str(sys.argv[1])+"_"+save_name+"_Images", images)
    np.save(str(sys.argv[1])+"_"+save_name+"_Labels", labels)
    print("\t\tALL DONE\n\t{} images loaded".format(numbers))

print("codeing .. started!\n\n")

print("=============================sections=============================")
print("reading and save to numpy file images\n")

print ("\tdata directory is :", str(sys.argv[1]))

folders_in_main_folder(str(sys.argv[1]), str(sys.argv[2]))

print("=============================save DONE=============================")
