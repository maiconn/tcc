def configurar_bluetooth(self, mac_addr=None):
    os.popen('sudo rfcomm release 0').read()
    if mac_addr is not None:
        port = self.bt_recuperar_servico_obd(mac_addr)
        if port is not None:
            os.system("sudo rfcomm bind 0 %s %s " % (addr, port))
            return True
        return False
    nearby_devices = bluetooth.discover_devices(
        duration=10, lookup_names=True, flush_cache=True, lookup_class=False)
    for addr, name in nearby_devices:
        port = self.bt_recuperar_servico_obd(addr)
        if port is not None:
            os.system("sudo rfcomm bind 0 %s %s " % (addr, port))
            return True
    return False

    