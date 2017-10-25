import RPi.GPIO as GPIO
import time, threading, os
from datetime import datetime, timedelta
from utils import *

class Led:
    BRANCO = 37
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
        GPIO.setup(Led.BRANCO, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.VERDE, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.AZUL, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(Led.VERMELHO, GPIO.OUT)   # Set LedPin's mode is output      
        GPIO.setup(self.PIN_BOTAO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    def destroy(self):
        GPIO.output(Led.BRANCO, GPIO.LOW)   # led off
        GPIO.output(Led.VERDE, GPIO.LOW)   # led off
        GPIO.output(Led.AZUL, GPIO.LOW)   # led off
        GPIO.output(Led.VERMELHO, GPIO.LOW)   # led off
    
    def pisca_led(self, led, vezes, tempo=0.2 ,aceso=True):
        while vezes > 0:
            self._pisca_led(led, tempo)
            vezes -= 1
        if aceso:
            self.acende_led(led)
    
    def pisca_todos_leds(self, qtd=0, tempo=0.4):
        for i in range(0,qtd):
            t = PiscaTodosLedsThread(self, tempo)
            t.start()
        t.stop()
    
    def apaga_todos_leds(self):
        GPIO.output(Led.BRANCO, GPIO.LOW)
        GPIO.output(Led.VERDE, GPIO.LOW)  
        GPIO.output(Led.AZUL, GPIO.LOW)  
        GPIO.output(Led.VERMELHO, GPIO.LOW) 

    def acende_led(self, led):
         GPIO.output(led, GPIO.HIGH)  # led on
    
    def apaga_led(self, led):
         GPIO.output(led, GPIO.LOW)  # led off

    def _pisca_led(self, led, tempo): 
        GPIO.output(int(led), GPIO.HIGH)  # led on
        time.sleep(tempo)
        GPIO.output(int(led), GPIO.LOW)  # led off
        time.sleep(tempo)

    def blink(self, led, tempo=0.2, aceso=True):
        t = PiscaLedThread(self, led, tempo, aceso)
        t.start()
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
    def __init__(self, gpio_control, tempo=0.2):
        self.stopped = False
        self.gpio_control = gpio_control
        self.tempo = tempo
        threading.Thread.__init__(self)

    def run(self):
        while not self.stopped:
            GPIO.output(Led.BRANCO, GPIO.HIGH)  # led on
            GPIO.output(Led.VERDE, GPIO.HIGH)  # led on
            GPIO.output(Led.AZUL, GPIO.HIGH)  # led on
            GPIO.output(Led.VERMELHO, GPIO.HIGH)  # led on
            time.sleep(self.tempo)
            GPIO.output(Led.BRANCO, GPIO.LOW)
            GPIO.output(Led.VERDE, GPIO.LOW)  
            GPIO.output(Led.AZUL, GPIO.LOW)  
            GPIO.output(Led.VERMELHO, GPIO.LOW) 
            time.sleep(self.tempo)
    
    def stop(self):
        self.stopped = True