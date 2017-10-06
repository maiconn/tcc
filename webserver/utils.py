import smtplib, time, io, os
from twilio.rest import Client
from flask import json
from collections import namedtuple
from python_obd.obd import obd, OBDStatus
 
"""
SIMULADOR:
            -1 = BUSCAR DAS CONFIGS
             0 = SEM SIMULADOR
             1 = OBDSIM
             2 = ECU Engine PRO
"""
_simulador = -1
_debug = True
_connection = None

class Status:
    def __init__(self, MIL, qtd_erros, tipo_ignicao):
        self.MIL = MIL
        self.qtd_erros = qtd_erros
        self.tipo_ignicao = tipo_ignicao

    def json_dump(self):
        return dict(MIL=self.MIL, qtd_erros=self.qtd_erros, tipo_ignicao=self.tipo_ignicao)

class StatusDTC:
    def __init__(self, registrados, pendentes, status):
        self.registrados = registrados
        self.pendentes = pendentes
        self.status = status

    def json_dump(self):
        return dict(dtc_registrados=self.registrados, dtc_pendentes=self.pendentes, status=self.status.json_dump())

def get_status_dtc(connection):
    simulador = get_simulador()
    log("get_status_dtc: "+str(simulador))

    dtc_registrados = connection.query_dtc(simulador=simulador)
    dtc_pendentes = connection.query_dtc(cmd=obd.commands.GET_CURRENT_DTC ,simulador=simulador) 
    status = connection.query(obd.commands.STATUS)
    status = status.value

    _registrados = []
    _pendentes = []
    for codigo, descricao in dtc_registrados:
        _registrados.append(dict(codigo=codigo, 
                                descricao=descricao, 
                                url='http://www.troublecodes.net/'+str(codigo)))

    for codigo, descricao in dtc_pendentes:
        _pendentes.append(dict(codigo=codigo, descricao=descricao, url='http://www.troublecodes.net/'+str(codigo)))

    _status = Status(MIL=status.MIL, qtd_erros=status.DTC_count, tipo_ignicao=status.ignition_type)
    status_dtc = StatusDTC(_pendentes, _registrados, _status)

    return status_dtc    

def get_configs():
        configs = None
        try:
            with io.open('./database/configs.txt', 'r') as f:
                content = f.read()
            configs = json.loads(content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))    
        except IOError as ex:
            if "No such file or directory" in str(ex):
                configs = None
            else:
                raise ex
        return configs

def send_sms(numero, mensagem):
        try:
            account_sid = "AC932104250d2379654fc7b969cd1d700d"
            auth_token  = "9f07c69be06f886c208be933e16b262b"

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to=numero, 
                from_="+16025669376",
                body=mensagem)

            log("SMS Enviada para %s | Mensagem: %s | SID: %s" % (numero, mensagem, message.sid))
        except Exception as ex:
            log("SMS ERROR: " + str(ex))

def send_email(email, mensagem):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("maicon.gerardi", "5158126-Ahuei1650")

        msg = "Te amo meu amor <3!" # The /n separates the message from the headers
        server.sendmail("maicon.gerardi@gmail.com", "jaine.stark@gmail.com", msg)

        log("Email Enviado para %s | Mensagem: %s" % (email, mensagem))
    except Exception as ex:
        log("EMAIL ERROR: " + str(ex))  

def log(message):
    if get_debug():
        print(message)

def set_debug(debug):
    global _debug
    _debug = debug

def get_debug():
    global _debug
    return _debug

def set_simulador(simulador):
    global _simulador
    _simulador = simulador

def get_simulador():
    #se for -1 pesquisa nas configs
    if _simulador == -1:
        configs = get_configs()

        #se nao tiver configs retorna sem simulador
        if(configs.simulador is None):
            return 0

        return int(configs.simulador)
    else:
        return int(_simulador)

def get_connection():
    global _connection
    if _connection is None:
        return _connect_obd()
    elif _connection.status() == OBDStatus.NOT_CONNECTED:
        return _connect_obd()
    else:
        return _connection

def _connect_obd():
    global _connection
    try:
        if get_debug():
            obd.logger.setLevel(obd.logging.DEBUG) 
            _connection = obd.OBD(baudrate=9600)
            log("protocolo: " + _connection.get_protocol_name())
        else:
            _connection = obd.OBD()

        if  _connection.status() == OBDStatus.NOT_CONNECTED:
            raise Excetion("nao conectado com ELM237.")

        return _connection
    except Exception as ex:
        _connection = None
        log("OBDERROR: " + str(ex))  
        return json.dumps(dict(error =  str(ex)))