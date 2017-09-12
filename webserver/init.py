from flask import Flask
from flask import json
import picamera
import base64
import serial
from coord import Coord
from pyobd.obd_capture import OBD_Capture
from datetime import datetime
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

obd_capture = OBD_Capture

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
    global obd_capture
    try:
        if not obd_capture.is_connected():
            connect_obdii()
            return json.dumps(dict(error =  "sem conexao, tentando reconectar..."))
    except Exception as se:
        connect_obdii()
        print('ERROR: ' + str(se))
        return json.dumps(dict(error =  str(se)))
    return json.dumps(obd_capture.capture())

@app.route('/get_dtc')
def get_dtc():
    global obd_capture
    return json.dumps(obd_capture.get_dtc())

def connect_obdii():
    global obd_capture
    try:
        obd_capture = OBD_Capture()
        obd_capture.connect()
        time.sleep(3)
        obd_capture.map_supported_pids()
        time.sleep(3)
    except Exception as se:
        print('OBDERROR: ' + str(se))

if __name__ == '__main__':    
    connect_obdii()
    app.run(debug=True, host='0.0.0.0')