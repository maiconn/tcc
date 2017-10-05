from flask import Flask, jsonify, request, json
import picamera, base64, serial, time, io, os, pdb, sys, getopt
from coord import Coord
from monitor_dtc import MonitorDTC
from datetime import datetime
from flask_cors import CORS
from pyobd_ffries import obd
from utils import *

connection = None
    
app = Flask(__name__)
CORS(app)

def main(argv):
    global connection

    _debug = True
    try:
        opts, args = getopt.getopt(argv,"sd:d:",["simulador=","debug="])
    except getopt.GetoptError:
        print('init.py -s <simulador(0,1,2)> -d <debug(0,1)>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--simulador"):
            set_simulador(int(arg))
        elif opt in ("-d", "--debug"):
            _debug = int(arg) == 1
    
    
    set_debug(_debug)
    log('_simulador: '+ str(get_simulador()))
    log('    _debug: '+ str(get_debug()))

    _config_pastas()
    _connect_obd()
    MonitorDTC(30, connection, get_debug())
    
    app.run(debug=_debug, host='0.0.0.0')

@app.route('/')
def index():
    return json.dumps(dict(status =  "OK"))

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
    log("connected to: " + port.portstr)

    count = 1
    while count < 15:
        try:
            rcv = port.read()
        except:
            rcv = ''

        line.append(rcv)

        if rcv == '\n':
            line = "".join(line)       
            log(line)
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

    if connection is None:
        _connect_obd()
        return json.dumps(dict(error =  "sem conexao, tentando reconectar..."))

    listSensors = []
    
    for command in connection.get_supported_commands():
        if command.command not in [ b"03", 
                                    b"07", 
                                    b"04", 
                                    b"0100", 
                                    b"0140", 
                                    b"0120",
                                    b"0100",
                                    b"0600",
                                    b"0101" ]: 
            cmd = command
            response = connection.query(cmd) 
            listSensors.append(dict(sensor = str(cmd), valor = str(response)))

    return json.dumps(listSensors)

@app.route('/get_dtc')
def get_dtc():
    global connection

    if connection is None:
        _connect_obd()
        return json.dumps(dict(error =  "sem conexao, tentando reconectar..."))

    return json.dumps(get_status_dtc(connection).json_dump())

@app.route('/save_configs', methods=['POST'])
def save_configs():
    try:
        content = request.get_json()
        with io.open('./database/configs.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False))
        return json.dumps(dict(status =  "OK"))
    except Exception as ex:
        return json.dumps(dict(error = str(ex)))

@app.route('/get_configs', methods=['GET'])
def configs():
    configs = "{}"
    try:
        _configs = get_configs()
        if _configs is not None:
            configs = _configs
    except IOError as ex:
        if "No such file or directory" in str(ex):
            configs = "{}"
    
    return configs

def _connect_obd():
    global connection
    try:
        if get_debug():
            obd.logger.setLevel(obd.logging.DEBUG) 
            connection = obd.OBD(baudrate=9600)
            log("protocolo: " + connection.get_protocol_name())
        else:
            connection = obd.OBD()
    except Exception as ex:
        connection = None
        log("OBDERROR: " + str(ex))  

def _config_pastas():
    if not os.path.exists("./database"):
        os.mkdir("./database", 0777)

if __name__ == '__main__':
    main(sys.argv[1:])