# /etc/rc.local

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)

def shutdown(channel):
    os.system("sudo shutdown -h now")
    
GPIO.add_event_detect(3, GPIO.FALLING, callback=shutdown)
while True:
    time.sleep(1)