Aplicação Para Monitoramento Veicular Em Tempo Real
==========
Origem
-------
Trabalho de conclusão do curso de Ciência da Computação da Universidade Regional de Blumenau (FURB), com a orientação do prof. Miguel Alexandre Wisintainer.

Introdução
-------
A aplicação foi desenvolvida para informar possíveis falhas mecânicas ou furtos no veículo. Ela possui como principais objetivos, visualizar a localização atual do automóvel, obter imagens e disponibilizar os dados de sua porta On-Board Diagnostic (OBD). Para isso, foi desenvolvido um software embarcado na placa Raspberry Pi Zero W utilizando como principais componentes um módulo Global Positioning System (GPS), um adaptador ELM327 Bluetooth e uma câmera. Para capturar os sensores e os códigos de erro do veículo, foi utilizada a biblioteca python-obd com o adaptador ELM327 Bluetooth. Também são enviadas notificações de e-mail e mensagens de texto caso ocorram falhas no automóvel. Os dados do software embarcado foram disponibilizados em um aplicativo móvel que utilizou a biblioteca Ionic para a sua construção.

Abstract
-------
The application has been developed to inform possible mechanical failure or theft in the vehicle. It has as main objectives, to visualize the current location of the car, to obtain images and to make available the data of its On-Board Diagnostic (OBD) port. For that, a software embedded in the Raspberry Pi Zero W board was developed using as main components a Global Positioning System (GPS) module, an ELM327 Bluetooth adapter and a camera. In order to capture the sensors and vehicle error codes, the python-obd library with the Bluetooth ELM327 adapter was used. E-mail notifications and text messages are also sent in the event of car failure. Embedded software data was made available in a mobile application that used the Ionic library for its construction. 

Tags
-------
Vehicle monitoring. Internet of things. IOT. On-board Diagnostic. OBD. OBDII. OBD2. DTC. Diagnostic Trouble Code. Failure notification. Geographic Positioning System. GPS. Raspberry Pi. ELM327.

Arquitetura da Aplicação
-------
!(/apresentação/2 - diagrama de arquitetura.png)
