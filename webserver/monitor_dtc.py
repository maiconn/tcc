from datetime import datetime, timedelta
from threading import Timer
from collections import namedtuple
from utils import *
import pdb

class MonitorDTC:
    debug = True
    seconds = 0
    delay = 0
    obd_control = None

    def __init__(self, seconds, obd_control):
        self.seconds = seconds
        self.obd_control = obd_control

        newDate = datetime.now() + timedelta(seconds=seconds)
        self.delay = (newDate - datetime.now()).total_seconds()

        self.start_monitor()

    def start_monitor(self):
        global executando_monitor
        while executando_monitor:
            time.sleep(1)

        t = Timer(self.delay, self.monitorar_dtcs)
        t.start()

    def monitorar_dtcs(self):
        global executando_monitor
        log("======iniciando monitorar_dtcs======")
        log(str(self.obd_control))
        try:
            executando_monitor = True

            # pdb.set_trace()
            configs = get_configs()
            if configs is None:
                raise Exception("Sem configuracoes...")
            log("configs: %s" % (str(configs)))

            connection = self.obd_control.get_connection()
            if not isinstance(connection, obd.OBD):
                raise Exception("Sem conexao obd2... " + str(connection))

            dtcs = self.obd_control.get_status_dtc(connection)
            log("dtcs_capturados: %s" % (str(dtcs.json_dump())))
            
            db_status = self.get_db_status()
            if db_status is None:
                db_status = []
                
            log("db_status: %s" % (str(db_status)))

            _novos_dtcs = []
            for dtc in dtcs.registrados:
                codigo = dtc.get('codigo')
                if codigo not in db_status:
                    _novos_dtcs.append(codigo)
            
            for dtc in dtcs.pendentes:
                codigo = dtc.get('codigo')
                if codigo not in db_status:
                    _novos_dtcs.append(codigo)

            _novos_dtcs = list(set(_novos_dtcs))
            log("_novos_dtcs: %s" % (str(_novos_dtcs)))

            notificou = True
            try:
                if len(_novos_dtcs) > 0 and configs.notificarSMS:
                    log('enviando notificacao sms para: '+ configs.celular)
                    send_sms(configs.celular, 'Codigos de erro encontrados em seu veiculo! '+str(_novos_dtcs))
            except Exception as ex:
                notificou = False
                log("[ERRO_SMS: MONITOR_DTC] "+ str(ex))
    
            try:
                if len(_novos_dtcs) > 0 and configs.notificarEmail:
                    log('enviando notificacao de e-mail para: '+ configs.email)
                    send_email(configs.email, 'Codigos de erro encontrados em seu veiculo! '+str(_novos_dtcs))
            except Exception as ex:
                notificou = False
                log("[ERRO_EMAIL: MONITOR_DTC] "+ str(ex))
        
            if notificou:
                if len(_novos_dtcs) > 0:
                    db_status += _novos_dtcs

                # pdb.set_trace()
                error = self.save_db_status(db_status).get("error")
                if error:
                    log("erro ao salvar status: " + error)
        except Exception as ex:
            log("MONITOR_DTC: "+str(ex))
        finally:
            executando_monitor = False
            log("=====finalizando monitorar_dtcs=====")
        
        self.start_monitor()

    def get_db_status(self):
        status = None
        try:
            with io.open('./database/status.txt', 'r') as f:
                content = f.read()
            if content is not None and content:
                status = json.loads(content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))    
        except IOError as ex:
            if "No such file or directory" in str(ex):
                status = None
            else:
                raise ex
        return status

    def save_db_status(self, status):
        try:
            with io.open('./database/status.txt', 'w', encoding='utf-8') as f:
                f.write(unicode(json.dumps(status, ensure_ascii=False)))
            return dict(status =  "OK")
        except Exception as ex:
            return dict(error = str(ex))