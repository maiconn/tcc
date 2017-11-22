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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Led.BRANCO_1, GPIO.OUT)
        GPIO.setup(Led.BRANCO_2, GPIO.OUT)
        GPIO.setup(Led.VERDE, GPIO.OUT)
        GPIO.setup(Led.AZUL, GPIO.OUT)
        GPIO.setup(Led.VERMELHO, GPIO.OUT)    
        GPIO.setup(self.PIN_BOTAO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        