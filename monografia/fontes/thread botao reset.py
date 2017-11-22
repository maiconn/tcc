def run(self):
    newDate = None
    intervalo = 0
    while not self.stopped:
        if GPIO.input(self.gpio_control.PIN_BOTAO) == 1:
            if not self.pressed:
                newDate = datetime.now() + timedelta(seconds=3)
                self.pressed = True
            else:
                intervalo = (newDate - datetime.now()).total_seconds()
                if intervalo <= 0:
                    print("HARDWARE RESETED BY USER...")
                    self.gpio_control.apaga_todos_leds()
                    self.mainFn(self.opt)
                    self.stop()
        else:
            self.pressed = False

            