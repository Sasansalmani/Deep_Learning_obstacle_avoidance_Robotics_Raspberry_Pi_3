import pygame as g
from cv2 import *
import string
import picamera as pc
import picamera.array

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

def action(dir, speed=1):
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
g.init()
j = g.joystick.Joystick(0)
j.init()

F = 0
B = 0
R = 0
L = 0
t_l = 0
t_r = 0
SPEED = 1
REC = 0
str = ""
pathImg = ""

#cap = VideoCapture(0)
cap = pc.PiCamera()
cap.resolution = (640, 480)
cap.framerate = 30
image = picamera.array.PiRGBArray(cap, size=(640, 480))

b_img = 0
f_img = 0
fl_img = 0
fr_img = 0
l_img = 0
r_img = 0
tl_img = 0
tr_img = 0

frames_time = 10

try:
    for img in cap.capture_continuous(image, format="bgr", use_video_port=True):
        #_, frame = cap.read()
        frame = img.array
        #imshow("image", frame)
        events = g.event.get()
        for event in events:
            if event.type == g.JOYBUTTONDOWN:
                #print(event.button, 'pressed')
                if event.button == 4:
                    REC = 1
                elif event.button == 5:
                    SPEED = 0
                elif event.button == 6:
                    t_l = 1
                elif event.button == 7:
                    t_r = 1
                elif event.button == 0:
                    j.quit
                    break
            elif event.type == g.JOYAXISMOTION:
                #print(event.axis, event.value)
                if event.axis == 1:
                    if event.value > 0.0:
                        B = 1
                    elif event.value < 0.0:
                        F = 1
                    elif event.value == 0.0:
                        B = 0
                        F = 0
                else:
                    if event.value > 0.0:
                        R = 1
                    elif event.value < 0.0:
                        L = 1
                    elif event.value == 0.0:
                        R = 0
                        L = 0
            elif event.type == g.JOYBUTTONUP:
                #print(event.button, 'released')
                if event.button == 4:
                    REC = 0
                elif event.button == 5:
                    SPEED = 1
                elif event.button == 6:
                    t_l = 0
                elif event.button == 7:
                    t_r = 0

        val = (F, B, R, L, SPEED)
        if REC == 1:
            if t_l == 1:
                str = ("TURN LEFT")
                imwrite(pathImg + "images/t_left/{}.{}".format(tl_img, 1) +".jpg", frame)
                action("tl", 2)
                tl_img += 1
            elif t_r == 1:
                str = ("TURN RIGHT")
                imwrite(pathImg + "images/t_right/{}.{}".format(tr_img, 1) +".jpg", frame)
                action("tr", 2)
                tr_img += 1
            elif val == (1,0,0,0,0):
                str = ("FRONT")
                imwrite(pathImg + "images/front/{}.{}".format(f_img, SPEED) +".jpg", frame)
                action("f", 1)
                f_img += 1
            elif val == (0,1,0,0,0):
                str = ("BACK")
                imwrite(pathImg + "images/back/{}.{}".format(b_img, SPEED) +".jpg", frame)
                action("b", 1)
                b_img +=1
            elif val == (0,0,1,0,0):
                str = ("RIGHT")
                imwrite(pathImg + "images/right/{}.{}".format(r_img, SPEED) + ".jpg", frame)
                action("r", 1)
                r_img += 1
            elif val == (0,0,0,1,0):
                str = ("LEFT")
                imwrite(pathImg + "images/left/{}.{}".format(l_img, SPEED) + ".jpg", frame)
                action("l", 1)
                l_img += 1
            elif val == (1,0,1,0,0):
                str = ("FRONT_RIGHT")
                imwrite(pathImg + "images/f_right/{}.{}".format(fr_img, SPEED) + ".jpg", frame)
                action("fr", 1)
                fr_img += 1
            elif val == (1,0,0,1,0):
                str = ("FRONT_LEFT")
                imwrite(pathImg + "images/f_left/{}.{}".format(fl_img, SPEED) + ".jpg", frame)
                action("fl", 1)
                fl_img += 1
            elif val == (0,1,1,0,0):
                str = ("BACK_RIGHT")
                action("br", 1)
            elif val == (0,1,0,1,0):
                str = ("BACK_LEFT")
                action("bl", 1)
            elif val == (0,0,0,0,0):
                str = ("STOP")
                action("s", 1)
            elif val == (1,0,0,0,1):
                str = ("FRONT.POWER")
                imwrite(pathImg + "images/front/{}.{}".format(f_img, SPEED) +".jpg", frame)
                action("f", 2)
                f_img += 1
            elif val == (0,1,0,0,1):
                str = ("BACK.POWER")
                imwrite(pathImg + "images/back/{}.{}".format(b_img, SPEED) +".jpg", frame)
                action("b", 2)
                b_img += 1
            elif val == (0,0,1,0,1):
                str = ("RIGHT.POWER")
                imwrite(pathImg + "images/right/{}.{}".format(r_img, SPEED) +".jpg", frame)
                action("r", 2)
                r_img += 1
            elif val == (0,0,0,1,1):
                str = ("LEFT.POWER")
                imwrite(pathImg + "images/left/{}.{}".format(l_img, SPEED) +".jpg", frame)
                action("l", 2)
                l_img += 1
            elif val == (1,0,1,0,1):
                str = ("FRONT_RIGHT.POWER")
                imwrite(pathImg + "images/f_right/{}.{}".format(fr_img, SPEED) +".jpg", frame)
                action("fr", 2)
                fr_img += 1
            elif val == (1,0,0,1,1):
                str = ("FRONT_LEFT.POWER")
                imwrite(pathImg + "images/f_left/{}.{}".format(fl_img, SPEED) +".jpg", frame)
                action("fl", 2)
                fl_img += 1
            elif val == (0,1,1,0,1):
                str = ("BACK_RIGHT.POWER")
                action("br", 2)
            elif val == (0,1,0,1,1):
                str = ("BACK_LEFT.POWER")
                action("bl", 2)
            elif val == (0,0,0,0,1):
                str = ("STOP")
                action("s", 2)
            waitKey(frames_time)
        elif REC == 0:
            if t_l == 1:
                action("tl", 2)
            elif t_r == 1:
                action("tr", 2)
            elif val == (1,0,0,0,0):
                action("f", 1)
            elif val == (0,1,0,0,0):
                action("b", 1)
            elif val == (0,0,1,0,0):
                action("r", 1)
            elif val == (0,0,0,1,0):
                action("l", 1)
            elif val == (1,0,1,0,0):
                action("fr", 1)
            elif val == (1,0,0,1,0):
                action("fl", 1)
            elif val == (0,1,1,0,0):
                action("br", 1)
            elif val == (0,1,0,1,0):
                action("bl", 1)
            elif val == (0,0,0,0,0):
                action("s", 1)
            elif val == (1,0,0,0,1):
                action("f", 2)
            elif val == (0,1,0,0,1):
                action("b", 2)
            elif val == (0,0,1,0,1):
                action("r", 2)
            elif val == (0,0,0,1,1):
                action("l", 2)
            elif val == (1,0,1,0,1):
                action("fr", 2)
            elif val == (1,0,0,1,1):
                action("fl", 2)
            elif val == (0,1,1,0,1):
                action("br", 2)
            elif val == (0,1,0,1,1):
                action("bl", 2)
            elif val == (0,0,0,0,1):
                action("s", 2)
            waitKey(frames_time)

        print(str)
        image.truncate(0)

except KeyboardInterrupt:
    print("exit")
    j.quit
