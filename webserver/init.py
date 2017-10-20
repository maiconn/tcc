import picamera, base64, serial, io, pdb, sys, getopt, numbers

from flask import Flask, jsonify, request, json
from flask_cors import CORS
from control.python_obd.obd import obd
from control.utils import *
from control.obd_control import ObdControl
from control.dtc_control import DTCControl
from control.bluetooth_control import BluetoothControl
    
app = Flask(__name__)
CORS(app)

obd_control = None
bluetooth_control = None

def main(argv):
    global obd_control
    _debug = True
    _monitor = False
    _log = True
    _btMacAddr = None
    try:
        opts, args = getopt.getopt(argv,"hd:s:m:l:a:",["help","simulador=","debug=","monitor=","log=","addr="])
    except getopt.GetoptError:
        print('usage: init.py [-s simulador] [-d debug]  [-m monitor] [-l log] [-a addr]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('usage: init.py [-s simulador] [-d debug]  [-m monitor] [-l log] [-a addr]')
            print("%s :   %s" % ("-s", "simulador utilizado"))
            print("          0 = SEM SIMULADOR")
            print("          1 = OBDSIM")
            print("          2 = ECU Engine PRO")
            print("          3 = BUSCAR DAS CONFIGS")
            print("%s :   %s" % ("-d", "debug: 1- ativo, 0-inativo"))
            print("%s :   %s" % ("-m", "monitor dtc: 1- ativo, 0-inativo"))
            print("%s :   %s" % ("-l", "log em arquivo: 1- ativo, 0-inativo"))
            print("%s :   %s" % ("-a", "MAC addr Bluetooth ELM327 ex: -a 00:1D:A5:00:00:14"))
            sys.exit(0)
            
        elif opt in ("-s", "--simulador"):
            set_simulador(int(arg))
        elif opt in ("-d", "--debug"):
            _debug = int(arg) == 1
        elif opt in ("-m", "--monitor"):
            _monitor = int(arg) == 1
        elif opt in ("-l", "--log"):
            _log = int(arg) == 1
        elif opt in ("-a", "--addr"):
            _btMacAddr = int(arg)

    configurar_log(_log)
    set_debug(_debug)
    log("==============>INICIANDO SERVIDOR<=============")
    log('_simulador: '+ str(get_simulador()))
    log('    _debug: '+ str(get_debug()))
    log('  _monitor: '+ str(_monitor))
    log('      _log: '+ str(_log))
    log('_btMacAddr: '+ str(_btMacAddr))

    config_pastas()

    bluetooth_control = BluetoothControl()
    if not bluetooth_control.configurar_bluetooth(_btMacAddr):
        log('servidor nao iniciado, causa: bluetooth nao configurado corretamente.')
        sys.exit(2)

    obd_control = ObdControl()
    
    if _monitor:
        DTCControl(20, obd_control)    

    app.run(debug=_debug, host='0.0.0.0', port=80)

@app.route('/')
def index():
    return json.dumps(dict(status =  "OK"))

@app.route('/get_foto')
def get_foto():
    camera = picamera.PiCamera()
    camera.rotation = 270
    camera.capture('./fotos/image1.jpg')
    camera.close()
    with open("./fotos/image1.jpg", "rb") as image_file:
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
                
                return json.dumps(dict(lat=lat, longit=longit))
            
            line = []
            count = count + 1

    return json.dumps(dict(error =  "Sem Dados na porta /dev/serial0"))

@app.route('/get_obdii')
def get_obdii():
    global obd_control
    connection = obd_control.get_connection()
    if not isinstance(connection, obd.OBD):
        log_error(str(connection))
        return connection

    listSensors = []
    
    for command in connection.get_supported_commands():
        if command.command not in [ b"03", 
                                    b"07", 
                                    b"04", 
                                    b"0100", 
                                    b"0120", 
                                    b"0140",
                                    b"0600",
                                    b"0620",
                                    b"0640",
                                    b"0660",
                                    b"0680",
                                    b"06A0",
                                    b"0101" ]: 
            cmd = command
            response = obd_control.execute_query(connection, cmd)

            valor = ""
            unidade = ""
            try:
                valor = response.value.magnitude
                if isinstance(valor, numbers.Real):
                    if valor % 1 == 0:
                        valor = int(valor)
                    else:
                        valor = str(float(str("%.4f" % round(valor,4))))

                else:
                    valor = str(valor)
                unidade = str(response.value.u)
            except AttributeError:
                valor = response.value
                unidade = ""
            listSensors.append(dict(sensor=str(cmd.desc), 
                                    valor=str(valor), 
                                    unidade=unidade, 
                                    codigo=str(cmd.command)))

    return json.dumps(sorted(listSensors, key=lambda s: s.get('codigo')))

@app.route('/get_dtc')
def get_dtc():
    # pdb.set_trace()
    global obd_control
    connection = obd_control.get_connection()
    if not isinstance(connection, obd.OBD):
        log_error(str(connection))
        return connection

    return json.dumps(obd_control.get_status_dtc(connection).json_dump())

@app.route('/save_configs', methods=['POST'])
def save_configs():
    try:
        content = request.get_json()
        with io.open('./database/configs.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False))
        return json.dumps(dict(status =  "OK"))
    except Exception as ex:
        log_error(str(ex))
        return json.dumps(dict(error = str(ex)))

@app.route('/get_configs', methods=['GET'])
def configs():
    try:
        # pdb.set_trace()
        configs = get_configs()
        if configs is not None:
            return json.dumps(configs.__dict__)
        else:
            return json.dumps(dict())
    except IOError as ex:
        if "No such file or directory" in str(ex):
            return json.dumps(dict())
    except Exception as ex2:
            log_error(str(ex2))
            return json.dumps(dict(error = str(ex2)))

if __name__ == '__main__':
    main(sys.argv[1:])