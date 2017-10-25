import RPi.GPIO as GPIO
import time
LebBranco = 37    
LedVerde = 35     
LedAzul = 33     
LedVermelho = 31    

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LebBranco, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LebBranco, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led

    GPIO.setup(LedVerde, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LedVerde, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led

    GPIO.setup(LedAzul, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LedAzul, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led

    GPIO.setup(LedVermelho, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LedVermelho, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led

    # GPIO.setmode(GPIO.BCM)      
    GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
def blink():
  while True:
    if GPIO.input(40) == 1:
        GPIO.output(LebBranco, GPIO.HIGH)  # led on
        GPIO.output(LedVerde, GPIO.HIGH)  # led on
        GPIO.output(LedAzul, GPIO.HIGH)  # led on
        GPIO.output(LedVermelho, GPIO.HIGH)  # led on
    else:
        GPIO.output(LebBranco, GPIO.LOW) # led off
        GPIO.output(LedVerde, GPIO.LOW)  # led off
        GPIO.output(LedAzul, GPIO.LOW)  # led off
        GPIO.output(LedVermelho, GPIO.LOW)  # led off

def destroy():
  GPIO.output(LebBranco, GPIO.LOW)   # led off
  GPIO.output(LedVerde, GPIO.LOW)   # led off
  GPIO.output(LedAzul, GPIO.LOW)   # led off
  GPIO.output(LedVermelho, GPIO.LOW)   # led off
  GPIO.cleanup()                  # Release resource
if __name__ == '__main__':     # Program start from here
  setup()
  try:
    blink()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()