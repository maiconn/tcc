thread_leds = PiscaLedThread(self.gpio_control, Led.BRANCO_1)
thread_leds.start()
while True:
	os.popen("sudo pkill -9 -f wvdial").read()
	time.sleep(1)
	os.popen("sudo wvdial tim &")
	time.sleep(7)
	ipPpp0 = str(os.popen("ifconfig ppp0 | grep inet")
		.read())
	    .replace("          inet end.: ", "")[:3]
	if int(ipPpp0) <= 100:
		self.gpio_control.pisca_led(Led.VERMELHO, tempo=1, aceso=False)
		continue
	break

thread_leds.stop()
thread_leds = PiscaLedThread(self.gpio_control, Led.BRANCO_1, tempo=0.05)
thread_leds.start()

os.popen("sudo pkill -9 -f noip2").read()
time.sleep(2)
os.popen("sudo noip2").read()

thread_leds.stop()
