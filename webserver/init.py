import picamera, base64, serial, io, pdb, sys, getopt, numbers, time, threading

from flask import Flask, jsonify, request, json, Response
from flask_cors import CORS
from control.python_obd.obd import obd
from control.utils import *
from control.obd_control import ObdControl
from control.dtc_control import DTCControl
from control.bluetooth_control import BluetoothControl
from control.gpio_control import GPIOControl, Led, PiscaLedThread, PiscaTodosLedsThread

from video_streaming.camera_pi import Camera
    
app = Flask(__name__)
CORS(app)

obd_control = None
bluetooth_control = None
gpio_control = None
my_camera = None
thread_leds = None

def main(argv):
    global obd_control
    global my_camera
    global gpio_control
    try:
        gpio_control = GPIOControl()
        t = PiscaTodosLedsThread(gpio_control, 0.1)
        t.start()
        time.sleep(1)
        t.stop()

        thread_leds = PiscaLedThread(gpio_control,Led.BRANCO)
        thread_leds.start()

        _debug = True
        _monitor = False
        _log = True
        _btMacAddr = None
        _ignorar = False
        try:
            opts, args = getopt.getopt(argv,"hd:s:m:l:a:i:",["help","simulador=","debug=","monitor=","log=","addr=","ignorar="])
        except getopt.GetoptError:
            print('usage: init.py [-s simulador] [-d debug]  [-m monitor] [-l log] [-a addr] [-i ignorar]')
            sys.exit(2)
        
        for opt, arg in opts:    
            if opt in ("-s", "--simulador"):
                set_simulador(int(arg))
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

        configurar_log(_log)
        set_debug(_debug)
        log("==============>INICIANDO SERVIDOR<=============")
        log('_simulador: '+ str(get_simulador()))
        log('    _debug: '+ str(get_debug()))
        log('  _monitor: '+ str(_monitor))
        log('      _log: '+ str(_log))
        log('_btMacAddr: '+ str(_btMacAddr))
        log('  _ignorar: '+ str(_ignorar))

        config_pastas()

        if not _ignorar:
            _connected = False
            _tentativas = 1
            _max_tentativas = 5
            while not _connected:
                log("====> iniciando conexoes [%so tentativa]" % str(_tentativas))
                try:
                    thread_leds.stop()
                    thread_leds = PiscaLedThread(gpio_control, Led.AZUL)
                    thread_leds.start()
                    log("=> iniciando conexao bluetooth")
                    bluetooth_control = BluetoothControl()
                    if not bluetooth_control.configurar_bluetooth(_btMacAddr):
                        raise Exception('bluetooth nao configurado corretamente.')
                   
                    thread_leds.stop()
                    thread_leds = PiscaLedThread(gpio_control, Led.VERDE)
                    thread_leds.start()

                    log("=> iniciando conexao obd2")
                    obd_control = ObdControl()
                    if _monitor:
                        log("=> iniciando monitor obd")
                        DTCControl(20, obd_control)
                    _connected = True
                    thread_leds.stop()
                except Exception as ex:
                    log_error('BT_OBR_ERR: %s.' % str(ex))
                    gpio_control.blink(Led.VERMELHO,  tempo=3, aceso=False)
                    if _tentativas >= _max_tentativas:
                        log_error('servidor nao iniciado, causa: %s.' % str(ex))
                        sys.exit(2)
                    _tentativas += 1
        else:
            log_warn("=> obd e bluetooth inativos")

        log("=> iniciando camera")
        my_camera = Camera()

        app.run(debug=_debug, host='0.0.0.0', port=80, threaded=True)
        # app.run(debug=_debug, host='0.0.0.0', port=80)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        stop_all()

def stop_all():
    global gpio_control
    global my_camera
    global thread_leds
    if gpio_control is not None:
        gpio_control.destroy()
    if my_camera is not None:
        my_camera.stop()
    if thread_leds is not None:
        thread_leds.stop()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def index():
    return json.dumps(dict(status =  "OK"))

@app.errorhandler(Exception)
def all_exception_handler(error):
    global gpio_control
    gpio_control.blink(Led.VERMELHO, aceso=False)
    log_exception(error)
    return 'Error', 500

@app.route('/get_foto')
def get_foto():
    global my_camera
    global gpio_control
    gpio_control.blink(Led.BRANCO)

    my_stream = io.BytesIO()
    encoded_string = base64.b64encode(my_camera.get_frame())
    return 'data:image/jpeg;base64,' + encoded_string


def gen(camera):
    """Video streaming generator function."""
    global gpio_control
    while True:
        t = gpio_control.blink_thread(Led.BRANCO,1)
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        finally:
            t.stop()

@app.route('/get_video')
def get_video():
    global my_camera
    return Response(gen(my_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_gps')
def get_gps():
    global gpio_control
    t = gpio_control.blink_thread(Led.VERDE)
    try:
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
    finally:
        t.stop()
    return json.dumps(dict(error =  "Sem Dados na porta /dev/serial0"))

@app.route('/get_obdii_pids')
def get_obdii_pids():
    global gpio_control
    t = gpio_control.blink_thread(Led.AZUL)
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
        gpio_control.blink(Led.VERMELHO,  tempo=1, aceso=False)
        return json.dumps(dict(error = str(ex)))
    finally:
        t.stop()

@app.route('/get_obdii_values')
def get_obdii_values():
    global obd_control
    global gpio_control
    t = gpio_control.blink_thread(Led.AZUL)
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
        gpio_control.blink(Led.VERMELHO,  tempo=1, aceso=False)
        return json.dumps(dict(error = str(ex)))
    finally:
        t.stop()

@app.route('/get_dtc')
def get_dtc():
    global obd_control
    global gpio_control
    t = gpio_control.blink_thread(Led.AZUL)
    try:
        return json.dumps(obd_control.get_status_dtc().json_dump())
    except Exception as ex:
        log_error(str(ex))
        gpio_control.blink(Led.VERMELHO, aceso=False)
        return json.dumps(dict(error = str(ex)))
    finally:
        t.stop()

@app.route('/clear_dtc')
def clear_dtc():
    global obd_control
    global gpio_control
    t = gpio_control.blink_thread(Led.AZUL)
    try:
        obd_control.execute_query(obd.commands.CLEAR_DTC)
        try:
            os.remove("./database/status.txt")
        except Exception as ex:
            if not "No such file or directory" in str(ex):
                raise Exception(ex)
        return json.dumps(dict(status =  "OK"))
    except Exception as ex:
        log_error(str(ex))
        gpio_control.blink(Led.VERMELHO, aceso=False)
        return json.dumps(dict(error = str(ex)))
    finally:
        t.stop()

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