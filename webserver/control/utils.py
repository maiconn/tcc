import smtplib, io, os, logging
from twilio.rest import Client
from flask import json
from collections import namedtuple
 
"""
SIMULADOR:
             0 = SEM SIMULADOR
             1 = OBDSIM
             2 = ECU Engine PRO
             3 = BUSCAR DAS CONFIGS
"""
_simulador = 3
_debug = True
_rootLogger = logging.getLogger()

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
        server.login("monitor.tcc2", "meumonitor")

        msg = 'Subject: {}\n\n{}'.format('[Monitor Do Veiculo] IMPORTANTE!', mensagem) 

        server.sendmail("monitor.tcc2@gmail.com", email, msg)

        print("Email Enviado para %s | Mensagem: %s" % (email, mensagem))
    except Exception as ex:
        print("EMAIL ERROR: " + str(ex))  

def configurar_log(logArquivo):
    global _rootLogger
    _rootLogger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter('[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
    if logArquivo:
        fileHandler = logging.FileHandler("{0}/{1}.log".format("./log", "monitor"))
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(logFormatter)
        _rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logFormatter)
    _rootLogger.addHandler(consoleHandler)


def log(message):
    global _rootLogger
    _rootLogger.info(message)

def log_warn(message):
    global _rootLogger
    _rootLogger.warn(message)

def log_error(message):
    global _rootLogger
    _rootLogger.error(message)

def log_exception(ex):
    global _rootLogger
    _rootLogger.error(ex, exc_info=True)

def config_pastas():
    if not os.path.exists("./database"):
        os.mkdir("./database", 0777)

    if not os.path.exists("./log"):
        os.mkdir("./log", 0777)

def get_configs():
        configs = None
        try:
            with io.open('./database/configs.txt', 'r') as f:
                content = f.read()
            if content is not None and content:
                configs = json.loads(content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))    
        except IOError as ex:
            if "No such file or directory" in str(ex):
                configs = None
            else:
                raise ex
        return configs

def set_debug(debug):
    global _debug
    if debug:
        _rootLogger.setLevel(logging.DEBUG)
    else:
        _rootLogger.setLevel(logging.INFO)
    _debug = debug

def get_debug():
    global _debug
    return _debug

def set_simulador(simulador):
    global _simulador
    _simulador = simulador

def get_simulador():
    #se for 3 pesquisa nas configs
    if _simulador == 3:
        configs = get_configs()

        #se nao tiver configs retorna sem simulador
        if(configs is None):
            return 0

        return int(configs.simulador)
    else:
        return int(_simulador)