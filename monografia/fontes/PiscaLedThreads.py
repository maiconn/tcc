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

        