def bt_recuperar_servico_obd(self, addr):
    services = bluetooth.find_service(address=addr)
    port = None
    if len(services) > 0:
        for svc in services:
            if(svc["protocol"] == "RFCOMM"):
                if("COM" in svc["name"] or
                    svc["name"] == "SPP" or
                    svc["name"] == "BLT"):
                    return int(svc["port"])
    return None


