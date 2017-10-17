# Copyright Jaimyn Mayer 2016 (known as "jabelone" online)
# pythonSB is released under a GPL v3 or later license, see this
# page for the full license: http://www.gnu.org/licenses/gpl-3.0.en.html
# This is part of pythonSB.  Github here: https://github.com/jabelone/pythonSB
# 
# This example file shows how to use all features of pythonSB.
#  
# 1000us/2000us is normally the extremes and 1500us is centered.
# Most servos have a range from about 1000us to about 2000us.
import pigpio
import time

servo=pigpio.pi()
#pi18.write(18,1)
#pi18.set_servo_pulsewidth(18,1000)
servo.set_PWM_frequency(24,50)
#servo.set_PWM_range(24, 1000)
servo.set_PWM_dutycycle(24,88)
#time.sleep(1)
#for i in range(38,139):
#    servo.set_PWM_dutycycle(24,i)
#    time.sleep(0.2)
#    print(i)
#servo.set_PWM_dutycycle(24,88.5)
#   time.sleep(1)
#servo.set_PWM_dutycycle(24,139)
#time.sleep(1)
servo.stop()


#servo_set(6, "1200us") #Set the servo attached to physical pin 12 on header 1 to 1500us.