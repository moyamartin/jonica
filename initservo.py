import RPi.GPIO as GPIO
import time

DC0=2.5
DC180=12.5
FServo=50


DCNeutral=(DC180+DC0)/2
m=(DC180-DC0)/180.0
h=DC0

GPIO.setmode(GPIO.BCM)

GPIO.setup(24,GPIO.OUT)

p = GPIO.PWM(24,FServo)
p.start(DCNeutral)
time.sleep(.5)
p.stop()
GPIO.cleanup()


