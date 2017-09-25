from flask import Flask
from flask import json
import picamera
import base64
import serial
from coord import Coord
from datetime import datetime
import time
from flask_cors import CORS
from pyobd_ffries import obd

app = Flask(__name__)
CORS(app)

connection = obd.OBD

@app.route('/')
def index():
    return 'WebServer No Ar... =D'

@app.route('/get_foto')
def get_foto():
    camera = picamera.PiCamera()
    camera.capture('./Fotos/image1.jpg')
    camera.close()
    with open("./Fotos/image1.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return 'data:image/jpeg;base64,' + encoded_string

@app.route('/get_gps')
def get_gps():
    port = serial.Serial("/dev/serial0", baudrate=9600, timeout=10.0)
    line = []
    print("connected to: " + port.portstr)

    count = 1
    while count < 15:
        try:
            rcv = port.read()
        except:
            rcv = ''

        line.append(rcv)

        if rcv == '\n':
            line = "".join(line)       
            print(line)
            if line.find("GPGGA") != -1: 
                retorno = line.split(',')

                if retorno[2] == '':
                    return json.dumps(dict(error =  "Sem Sinal"))

                lat = int(retorno[2][0:2]) + (float(retorno[2][2:len(retorno[2])]) / 60)
                if retorno[3] == 'S' :
                    lat = lat * -1
                
                longit = int(retorno[4][0:3]) + (float(retorno[4][3:len(retorno[4])]) / 60)
                if retorno[5] == 'W':
                    longit = longit * -1
                
                return json.dumps(Coord(lat, longit).json_dump())
            
            line = []
            count = count + 1

    return json.dumps(dict(error =  "Sem Dados na porta /dev/serial0"))

@app.route('/get_obdii')
def get_obdii():
    global connection

    listSensors = []
    
    for command in connection.get_supported_commands():
        if command.command not in [ b"03", 
                                    b"07", 
                                    b"04", 
                                    b"0100", 
                                    b"0140", 
                                    b"0120",
                                    b"0100",
                                    b"0600" ]: 
            cmd = command
            response = connection.query(cmd) 
            listSensors.append(dict(sensor = str(cmd), valor = str(response)))

    return json.dumps(listSensors)

@app.route('/get_dtc')
def get_dtc():
    global connection
    cmd = obd.commands.GET_DTC
    response = connection.query(cmd) 
    return str(response)

if __name__ == '__main__':  
    obd.logger.setLevel(obd.logging.DEBUG) 
    connection = obd.OBD()
    app.run(debug=True, host='0.0.0.0')