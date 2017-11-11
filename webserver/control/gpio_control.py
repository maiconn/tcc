import RPi.GPIO as GPIO
import time, threading, os
from datetime import datetime, timedelta
from utils import *

class Led:
    BRANCO_1 = 29
    BRANCO_2 = 37
    VERDE = 33
    AZUL = 35
    VERMELHO = 31

class GPIOControl:
    PIN_BOTAO = 40
    def __init__(self):
        self.setup()

    def setup(self):  
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(Led.BRANCO_1, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.BRANCO_2, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.VERDE, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.AZUL, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.VERMELHO, GPIO.OUT)   # Set LedPin's mode is output      
        GPIO.setup(self.PIN_BOTAO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    def destroy(self):
        GPIO.output(Led.BRANCO_1, GPIO.LOW)   # led off
        GPIO.output(Led.BRANCO_2, GPIO.LOW)   # led off
        GPIO.output(Led.VERDE, GPIO.LOW)   # led off
        GPIO.output(Led.AZUL, GPIO.LOW)   # led off
        GPIO.output(Led.VERMELHO, GPIO.LOW)   # led off
    
    def pisca_led(self, led, vezes=1, tempo=0.2 ,aceso=True):
        while vezes > 0:
            self._pisca_led(led, tempo)
            vezes -= 1
        if aceso:
            self.acende_led(led)
    
    def apaga_todos_leds(self):
        GPIO.output(Led.BRANCO_1, GPIO.LOW)
        GPIO.output(Led.BRANCO_2, GPIO.LOW)
        GPIO.output(Led.VERDE, GPIO.LOW)  
        GPIO.output(Led.AZUL, GPIO.LOW)  
        GPIO.output(Led.VERMELHO, GPIO.LOW) 

    def acende_todos_leds(self):
        GPIO.output(Led.BRANCO_1, GPIO.HIGH)
        GPIO.output(Led.BRANCO_2, GPIO.HIGH)
        GPIO.output(Led.VERDE, GPIO.HIGH)  
        GPIO.output(Led.AZUL, GPIO.HIGH)  
        GPIO.output(Led.VERMELHO, GPIO.HIGH) 

    def acende_led(self, led):
         GPIO.output(led, GPIO.HIGH)  # led on
    
    def apaga_led(self, led):
         GPIO.output(led, GPIO.LOW)  # led off

    def _pisca_led(self, led, tempo): 
        GPIO.output(int(led), GPIO.HIGH)  # led on
        time.sleep(tempo)
        GPIO.output(int(led), GPIO.LOW)  # led off
        time.sleep(tempo)

    def blink(self, led, tempo=0.2, aceso=True, tempo_piscando=0.1):
        t = PiscaLedThread(self, led, tempo, aceso)
        t.start()
        time.sleep(tempo_piscando)
        t.stop()
    
    def blink_thread(self, led, tempo=0.2, aceso=True):
        t = PiscaLedThread(self, led, tempo, aceso)
        t.start()
        return t


class PiscaLedThread(threading.Thread):
    def __init__(self, gpio_control, led, tempo=0.2, aceso=True):
        self.stopped = False
        self.gpio_control = gpio_control
        self.led = led
        self.tempo = tempo
        self.aceso = aceso
        threading.Thread.__init__(self)

    def run(self):
        while not self.stopped:
            GPIO.output(self.led, GPIO.HIGH)  # led on
            time.sleep(self.tempo)
            GPIO.output(self.led, GPIO.LOW)  # led off
            time.sleep(self.tempo)
        if self.aceso:
                GPIO.output(self.led, GPIO.HIGH)  # led on
    
    def stop(self):
        self.stopped = True

class PiscaTodosLedsThread(threading.Thread):
    def __init__(self, gpio_control, tempo=0.2, aceso=False, acender_vermelho=True):
        self.stopped = False
        self.gpio_control = gpio_control
        self.aceso = aceso
        self.acender_vermelho = acender_vermelho
        self.tempo = tempo
        threading.Thread.__init__(self)

    def run(self):
        while not self.stopped:
            self.acende()
            time.sleep(self.tempo)
            self.gpio_control.apaga_todos_leds()
            time.sleep(self.tempo)
            if self.aceso:
                self.acende()

    def acende(self):
        GPIO.output(Led.BRANCO_1, GPIO.HIGH)
        GPIO.output(Led.BRANCO_2, GPIO.HIGH)
        GPIO.output(Led.VERDE, GPIO.HIGH)  
        GPIO.output(Led.AZUL, GPIO.HIGH)  
        if self.acender_vermelho:
            GPIO.output(Led.VERMELHO, GPIO.HIGH) 

    def stop(self):
        self.stopped = True