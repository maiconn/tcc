import RPi.GPIO as GPIO
import time, os, threading, sys, getopt
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
from control.gpio_control import GPIOControl, PiscaTodosLedsThread, Led, PiscaLedThread

class VerificaResetThread(threading.Thread):
    def __init__(self, gpio_control, mainFn, opts):
        self.stopped = False
        self.pressed = False
        self.gpio_control = gpio_control
        self.mainFn = mainFn
        self.opt = opts

        threading.Thread.__init__(self)

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
    
    def stop(self):
        self.stopped = True

class ThreadPiscaPrimeiroLed(threading.Thread):
    def __init__(self, gpio_control):
        self.stopped = False
        self.gpio_control = gpio_control
        threading.Thread.__init__(self)

    def run(self):
        newDate = None
        intervalo = 0
        newDate = datetime.now() + timedelta(seconds=35)
        while not self.stopped:
            intervalo = (newDate - datetime.now()).total_seconds()
            if intervalo <= 0:
                self.stop()
            else:
                self.gpio_control.pisca_led(Led.BRANCO_1, tempo=0.05)
    
    def stop(self):
        self.stopped = True

class ConfiguracaoModemENoIpThread(threading.Thread):
    def __init__(self, gpio_control):
        self.stopped = False
	self.gpio_control = gpio_control
        threading.Thread.__init__(self)

    def run(self):
        thread_leds = PiscaLedThread(self.gpio_control, Led.BRANCO_1)
        thread_leds.start()

        while True:
            print("====> iniciando rede e configurando noip")
            print("==> discando")
            print("" + os.popen("sudo pkill -9 -f wvdial").read())
            time.sleep(1)
            os.popen("sudo wvdial tim &")
            time.sleep(7)
            print("==> verificando ip")     
            ipPpp0 = str(os.popen("ifconfig ppp0 | grep inet").read()).replace("          inet end.: ", "")[:3]
            if int(ipPpp0) <= 100:
                print(ipPpp0)
                self.gpio_control.pisca_led(Led.VERMELHO, tempo=1, aceso=False)
                continue
            break

        thread_leds.stop()
        thread_leds = PiscaLedThread(self.gpio_control, Led.BRANCO_1, tempo=0.05)
        thread_leds.start()
        print("" + os.popen("route add default ppp0").read())
        print("" + os.popen("curl https://ipinfo.io/ip").read())
        print("==> configurando noip")
        print("" + os.popen("sudo pkill -9 -f noip2").read())
        time.sleep(2)
        os.popen("sudo noip2").read()
        time.sleep(5)
        os.popen("sudo noip2 -S").read()
        
        thread_leds.stop()
        
    
    def stop(self):
        self.stopped = True

def main(argv):
    _debug = True
    _monitor = False
    _log = True
    _btMacAddr = None
    _ignorar = False
    _simulador = 3

    gpio_control = GPIOControl()
    t = PiscaTodosLedsThread(gpio_control, 0.1)
    time.sleep(1)
    t.start()

    print("   " + os.popen("sudo pkill -9 -f 'init.py'").read())
    try:
        opts, args = getopt.getopt(argv,"hd:s:m:l:a:i:",["help","simulador=","debug=","monitor=","log=","addr=","ignorar="])
         
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print('usage: power_on.py [-s simulador] [-d debug]  [-m monitor] [-l log] [-a addr]')
                print("%s :   %s" % ("-s", "simulador utilizado"))
                print("          0 = SEM SIMULADOR")
                print("          1 = OBDSIM")
                print("          2 = ECU Engine PRO")
                print("          3 = BUSCAR DAS CONFIGS")
                print("%s :   %s" % ("-d", "debug: 1- ativo, 0-inativo"))
                print("%s :   %s" % ("-m", "monitor dtc: 1- ativo, 0-inativo"))
                print("%s :   %s" % ("-l", "log em arquivo: 1- ativo, 0-inativo"))
                print("%s :   %s" % ("-a", "MAC addr Bluetooth ELM327 ex: -a 00:1D:A5:00:00:14"))
                print("%s :   %s" % ("-i", "ignorar obd: 1-sim, 0-nao"))
                sys.exit(0)
                
            elif opt in ("-s", "--simulador"):
                _simulador = (int(arg))
            elif opt in ("-d", "--debug"):
                _debug = int(arg) == 1
            elif opt in ("-m", "--monitor"):
                _monitor = int(arg) == 1
            elif opt in ("-l", "--log"):
                _log = int(arg) == 1
            elif opt in ("-a", "--addr"):
                _btMacAddr = int(arg)
            elif opt in ("-i", "--ignorar"):
                _ignorar = int(arg) == 1

        VerificaResetThread(gpio_control, main, argv).start()
        t.stop()

        ConfiguracaoModemENoIpThread(gpio_control).start()

        p = Popen(['python', 'init.py'] + argv, stdout=PIPE)
        p.stdout.close()
    except KeyboardInterrupt:
        sys.exit(2)
    except getopt.GetoptError:
        print('usage: power_on.py [-s simulador] [-d debug]  [-m monitor] [-l log] [-a addr] [-i ignorar]')
        sys.exit(2)
        
if __name__ == '__main__':
    main(sys.argv[1:])
