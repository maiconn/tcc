from datetime import datetime, timedelta
from threading import Timer
from utils import get_configs, get_status_dtc, log

class MonitorDTC:
    debug = True
    seconds = 0
    connection = None
    delay = 0

    def __init__(self, seconds, connection, debug):
        self.seconds = seconds
        self.connection = connection
        self.debug = debug

        newDate = datetime.now() + timedelta(seconds=seconds)
        self.delay = (newDate - datetime.now()).total_seconds()

        self.start_monitor()

    def start_monitor(self):
        t = Timer(self.delay, self.monitorar_dtcs)
        t.start()

    def monitorar_dtcs(self):
        log("======iniciando monitorar_dtcs======")
        configs = get_configs()
        log("configs: %s" % (str(configs)))

        dtc = get_status_dtc(self.connection())
        log("dtcs: %s" % (str(dtc.json_dump())))
        
        log("=====finalizando monitorar_dtcs=====")
        self.start_monitor()