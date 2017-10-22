import threading

from python_obd.obd import obd, OBDStatus
from utils import *

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
        status = None
        if self.status is not None:
            status = self.status.json_dump()
        return dict(dtc_registrados=self.registrados, dtc_pendentes=self.pendentes, status=status)

class ObdControl:
    _lock_comandos = threading.Lock()
    _lock_connection = threading.Lock()
    _supported_pids = None
    _connection = None

    def __init__(self, initObd=True):
        if initObd:
            self._connection = self.get_connection()
            self._supported_pids = self.get_supported_pids()

    def execute_query(self, cmd):
        connection = self.get_connection()
        with self._lock_comandos:
            return self._connection.query(cmd)

    def get_status_dtc(self):
        connection = self.get_connection()
        with self._lock_comandos:
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
            
            _status = None
            if status is not None:
                _status = Status(MIL=status.MIL, qtd_erros=status.DTC_count, tipo_ignicao=status.ignition_type)
            
            status_dtc = StatusDTC(_pendentes, _registrados, _status)
            return status_dtc

    def get_connection(self):
        with self._lock_connection:
            if self._connection is None:
                return self._connect_obd()
            elif self._connection.status() == OBDStatus.NOT_CONNECTED:
                return self._connect_obd()
            else:
                return self._connection

    def get_supported_pids(self):
        if self._supported_pids is not None:
            return self._supported_pids

        connection = self.get_connection()


        with self._lock_comandos:
            self._supported_pids = []
            for command in connection.get_supported_commands():
                if command.command not in [ b"03", 
                                            b"07", 
                                            b"04", 
                                            b"0100", 
                                            b"0120", 
                                            b"0140",
                                            b"0600",
                                            b"0620",
                                            b"0640",
                                            b"0660",
                                            b"0680",
                                            b"06A0",
                                            b"0101" ]:
                    self._supported_pids.append(command)
        return self._supported_pids

    def _connect_obd(self):
        try:
            if get_debug():
                obd.logger.setLevel(obd.logging.DEBUG) 
                self._connection = obd.OBD(baudrate=9600)
                log("protocolo: " + self._connection.get_protocol_name())
            else:
                self._connection = obd.OBD()

            if  self._connection.status() == OBDStatus.NOT_CONNECTED:
                raise Exception("nao conectado com ELM237.")

            return self._connection
        except Exception as ex:
            self._connection = None
            raise Exception(ex)