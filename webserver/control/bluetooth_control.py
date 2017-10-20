import bluetooth, os
from utils import *

class BluetoothControl:
    def configurar_bluetooth(self, mac_addr=None):
        # release rfcomm
        log(os.popen('sudo rfcomm release 0').read())

        # verificar se foi informado addr
        if mac_addr is not None:
            port = self.bt_recuperar_servico_obd(mac_addr)
            if port is not None:
                self.bt_bind_service(mac_addr, port)
                return True
            return False

        nearby_devices = bluetooth.discover_devices(
            duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

        log("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
            log("%s - %s" % (addr, name))

            port = self.bt_recuperar_servico_obd(addr)
            
            if port is not None:
                self.bt_bind_service(addr, port)
                return True
        
        return False

    def bt_recuperar_servico_obd(self, addr):
        services = bluetooth.find_service(address=addr)
        port = None
        if len(services) > 0:
            for svc in services:
                if(svc["protocol"] == "RFCOMM"):
                    if("COM" in svc["name"]):
                        return int(svc["port"])
                    if(svc["name"] == "BLT"):
                        return int(svc["port"])
        return None

    def bt_bind_service(self, addr, port):
        log("   PORT: " + str(port))
        os.system("sudo rfcomm bind 0 %s %s " % (addr, port))
        log("   " + os.popen('rfcomm').read())