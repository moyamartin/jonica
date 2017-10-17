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


def set_angle(angle):
	global m
	global h
	return (m*angle + h)
 

i = 0.0
try:
	while True:
		time.sleep(.5)
		setpoint = set_angle(i)
		p.ChangeDutyCycle(setpoint)
		print(i)
		i = i + 20.0
		if(i == 200.0):
			i = 0.0


except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()


