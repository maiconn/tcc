def _connect_obd(self):
    try: 
        self._connection = obd.OBD(baudrate=9600,portstr='/dev/rfcomm0',fast=False)
        if  self._connection.status() == OBDStatus.NOT_CONNECTED:
            raise Exception("nao conectado com ELM327.")
        return self._connection
    except Exception as ex:
        self._connection = None
        raise Exception(ex)

