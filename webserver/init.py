import picamera, base64, serial, io, pdb, sys, getopt, numbers, time

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

    log("=> iniciando conexao bluetooth")
    bluetooth_control = BluetoothControl()
    if not bluetooth_control.configurar_bluetooth(_btMacAddr):
        log('servidor nao iniciado, causa: bluetooth nao configurado corretamente.')
        sys.exit(2)

    log("=> iniciando conexao obd2")
    try:
        obd_control = ObdControl()
    except Exception as ex:
        log('servidor nao iniciado, causa: OBD2: %s.' % str(ex))
        sys.exit(2)
    
    if _monitor:
        DTCControl(20, obd_control)    

    app.run(debug=_debug, host='0.0.0.0', port=80, threaded=True)
    # app.run(debug=_debug, host='0.0.0.0', port=80)

@app.route('/')
def index():
    return json.dumps(dict(status =  "OK"))

@app.route('/get_foto')
def get_foto():
    my_stream = io.BytesIO()
    encoded_string = ""
    with picamera.PiCamera() as camera:
        # camera.rotation = 270
        camera.start_preview()
        time.sleep(2)
        camera.capture(my_stream, 'jpeg')
        my_stream.seek(0)
        encoded_string = base64.b64encode(my_stream.read())
        
    return 'data:image/jpeg;base64,' + encoded_string

@app.route('/get_video')
def get_foto():
    my_stream = io.BytesIO()
    encoded_string = ""
    with picamera.PiCamera() as camera:
        camera.resolution = (160, 120)
        camera.start_preview()
        camera.capture(my_stream, 'jpeg')
        my_stream.seek(0)
        encoded_string = base64.b64encode(my_stream.read())
        
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

@app.route('/get_obdii_pids')
def get_obdii_pids():
    global obd_control
    try:
        listPids = []
        for command in obd_control.get_supported_pids():
            cmd = command
            response = obd_control.execute_query(cmd)
            unidade = ""
            try:
                unidade = str(response.value.u)
            except AttributeError:
                unidade = ""
            listPids.append(dict(sensor=str(cmd.desc),
                                 unidade=unidade, 
                                 codigo=str(cmd.command),
                                 valor="0"))
        return json.dumps(sorted(listPids, key=lambda s: s.get('codigo')))
    except Exception as ex:
        log_error(str(ex))
        return json.dumps(dict(error = str(ex)))

@app.route('/get_obdii_values')
def get_obdii_values():
    global obd_control
    try:
        listSensors = []
        
        for command in obd_control.get_supported_pids():
            cmd = command
            response = obd_control.execute_query(cmd)

            valor = ""
            try:
                valor = response.value.magnitude
                if isinstance(valor, numbers.Real):
                    if valor % 1 == 0:
                        valor = int(valor)
                    else:
                        valor = str(float(str("%.4f" % round(valor,4))))
                else:
                    valor = str(valor)
            except AttributeError:
                valor = response.value
            listSensors.append(dict(codigo=str(cmd.command),
                                    valor=str(valor)))

        return json.dumps(sorted(listSensors, key=lambda s: s.get('codigo')))
    except Exception as ex:
        log_error(str(ex))
        return json.dumps(dict(error = str(ex)))

@app.route('/get_dtc')
def get_dtc():
    # pdb.set_trace()
    global obd_control
    try:
        return json.dumps(obd_control.get_status_dtc().json_dump())
    except Exception as ex:
        log_error(str(ex))
        return json.dumps(dict(error = str(ex)))

    

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