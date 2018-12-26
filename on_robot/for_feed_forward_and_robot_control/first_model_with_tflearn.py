import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np
import time
import picamera as pc
import picamera.array
import cv2

command = {0:"b", 1:"fl", 2:"fr", 3:"f", 4:"l", 5:"r", 6:"tl", 7:"tr"}

# X = X.reshape([-1,224,224,3])
# test_x = test_x.reshape([-1,224,224,3])

### ++++++++++++ set ports
import RPi.GPIO as gp
gp.setmode(gp.BCM)

motorPins = {"M1L": 20, "M1R": 21, "M2L": 5, "M2R": 6, "M3L": 13, "M3R": 19}

for pin in motorPins:
    gp.setup(motorPins[pin], gp.OUT)

frequency = 100

PWM1L = gp.PWM(motorPins["M1L"],frequency)
PWM1R = gp.PWM(motorPins["M1R"],frequency)
PWM2L = gp.PWM(motorPins["M2L"],frequency)
PWM2R = gp.PWM(motorPins["M2R"],frequency)
PWM3L = gp.PWM(motorPins["M3L"],frequency)
PWM3R = gp.PWM(motorPins["M3R"],frequency)

motorPWM = {"M1L": PWM1L, "M1R": PWM1R, "M2L": PWM2L, "M2R": PWM2R, "M3L": PWM3L, "M3R": PWM3R}

#   start pwm with 0 dutycycle
for pin in motorPWM:
    motorPWM[pin].start(0)

def set_pwm(pin, dutycycle):
    if dutycycle > 100:
        dutycycle = 100
    elif dutycycle < 0:
        dutycycle = 0
    pin.ChangeDutyCycle(dutycycle)

def action(dir, speed=2):
    if dir == "f":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*50)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*50)
    elif dir == "b":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*50)
        set_pwm(motorPWM["M3L"], speed*50)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "r":
        set_pwm(motorPWM["M1L"], speed*50)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*50)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*50)
    elif dir == "l":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*50)
        set_pwm(motorPWM["M2L"], speed*50)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*50)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "fr":
        set_pwm(motorPWM["M1L"], speed*50)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*50)
    elif dir == "fl":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*50)
        set_pwm(motorPWM["M2L"], speed*50)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "br":
        set_pwm(motorPWM["M1L"], speed*50)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*50)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "bl":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*50)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*50)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "s":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "tl":
        set_pwm(motorPWM["M1L"], speed*50)
        set_pwm(motorPWM["M1R"], speed*0)
        set_pwm(motorPWM["M2L"], speed*50)
        set_pwm(motorPWM["M2R"], speed*0)
        set_pwm(motorPWM["M3L"], speed*50)
        set_pwm(motorPWM["M3R"], speed*0)
    elif dir == "tr":
        set_pwm(motorPWM["M1L"], speed*0)
        set_pwm(motorPWM["M1R"], speed*50)
        set_pwm(motorPWM["M2L"], speed*0)
        set_pwm(motorPWM["M2R"], speed*50)
        set_pwm(motorPWM["M3L"], speed*0)
        set_pwm(motorPWM["M3R"], speed*50)


# +++++++++++++++ video capture
cap = pc.PiCamera()
cap.resolution = (640, 480)
cap.framerate = 30
image = picamera.array.PiRGBArray(cap, size=(640, 480))



convnet = input_data(shape=[None, 224,224,3], name='input')
convnet = conv_2d(convnet, 32, 5, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 32, 5, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 64, 5, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = fully_connected(convnet, 2*1024, activation='relu')
convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)
convnet = fully_connected(convnet, 8, activation='softmax')
convnet = regression(convnet, optimizer='sgd', learning_rate=0.01, loss='categorical_crossentropy', name='target')
model = tflearn.DNN(convnet)

model.load('Model.model')

for img in cap.capture_continuous(image, format="bgr", use_video_port=True):
    frame = img.array
    frame_ = cv2.resize(frame, (224,224))
    test = np.reshape(frame_, [1,224,224,3])
    #test = np.zeros([1,224,224,3])
    t = time.time()
    pred = model.predict(test)
    print(pred)
    act = command.get(np.argmax(pred))
    print(act)
    action(act, 2)
    print(time.time()-t)
    image.truncate(0)


