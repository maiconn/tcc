# Application For Real-Time Vehicle Monitoring
[README](README_EN.md) | [LEIA-ME](README.md)

- <a href="https://youtu.be/3hla2eGgnB4">Demo</a>
- [Presentation](/apresentação/tcc_bcc_2017_2_mmgsilva_MaiconMachadoGerardiDaSilva-AP.pdf)
- [Monography (PT-BR)](https://github.com/maiconn/tcc/raw/master/monografia/VF%20-%20Ajustes%20Finais/tcc_bcc_2017_2_mmgsilva_MaiconMachadoGerardiDaSilva-VF.pdf)

### What is?
An application that covers:
- A **embedded software** on a Raspberry Pi Zero W board to collect the geographic position, camera images and OBD port data from a car
- A **mobile application** to capture the information of this embedded software

### Principais Funcionalidades
* Vehicle images in real time
* Geographic position
* OBD2 port data:
   * Sensors (All)
   * Diagnostic Trouble Code (DTCs)
* Inform status of execution of the embedded server by means of LEDs
* Notify the user via text messages and email in case of DTC failures

### Origin
Completion of the Computer Science course of the Universidade Regional de Blumenau (FURB), with the orientation of prof. Miguel Alexandre Wisintainer.

### Tags 
Vehicle monitoring. Internet of things. IOT. On-board Diagnostic. OBD. OBDII. OBD2. DTC. Diagnostic Trouble Code. Failure notification. Geographic Positioning System. GPS. Raspberry Pi. ELM327.

## Introdução
The application has been developed to inform possible mechanical failure or theft in the vehicle. It has as main objectives, to visualize the current location of the car, to obtain images and to make available the data of its On-Board Diagnostic (OBD) port. For that, a software embedded in the Raspberry Pi Zero W board was developed using as main components a Global Positioning System (GPS) module, an ELM327 Bluetooth adapter and a camera. In order to capture the sensors and vehicle error codes, the python-obd library with the Bluetooth ELM327 adapter was used. E-mail notifications and text messages are also sent in the event of car failure. Embedded software data was made available in a mobile application that used the Ionic library for its construction.

## Hardwares Used
- Raspberry Pi Zero W
- Adaptador ELM327 Bluetooth
- GPS Ubox GY-GPS6MV2
- Raspberry Pi Camera 1.3
- Modem USB 3G ZTE MF626
- TIM brazilian operator chip
- LEDs
- Buttons Switch

## Application Architecture
<kbd>
  <img src="/apresentação/2%20-%20diagrama%20de%20arquitetura.png">
</kbd>

## Vehicle Installation
<kbd>
  <img src="/docs/install.png">
</kbd>

## App
| Location | OBD2 Sensors  | DTC Errors |
| ------------- | ------------- | ------------- |
| <img src="/docs/localizacao.png">| <img src="/docs/sensores.png"> | <img src="/docs/dtcs.png"> |

| Images / Streaming |
| ------------- |
| <img src="/docs/camera.png"> |
