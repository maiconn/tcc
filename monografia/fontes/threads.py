01 _lock_connection = threading.Lock()
02 
03 def get_connection(self):
04 	with self._lock_connection:
05 		if self._connection is None:
06 			return self._connect_obd()
07 		elif self._connection.status() == OBDStatus.NOT_CONNECTED:
08 			return self._connect_obd()
09 		else:
10 			return self._connection