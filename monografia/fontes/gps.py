@app.route('/get_gps')
def get_gps():
	port = serial.Serial("/dev/serial0", baudrate=9600, timeout=10.0)
    line = []
    count = 1
    while count < 15:
        try:
            rcv = port.read()
        except:
            rcv = ''
        line.append(rcv)
        if rcv == '\n':
            line = "".join(line)
            if line.find("GPGGA") != -1: 
                retorno = line.split(',')
                if retorno[2] == '':
                    return json.dumps(dict(error =  "Sem Sinal"))
                lat = int(retorno[2][0:2]) + (float(retorno[2][2:len(retorno[2])]) / 60)
                if retorno[3] == 'S' :
                    lat = lat * -1
                longit = int(retorno[4][0:3]) + (float(retorno[4][3:len(retorno[4])]) / 60)
                if retorno[5] == 'W':
                    longit = longit * -1
                return json.dumps(dict(lat=lat, longit=longit))
            line = []
            count = count + 1
    return json.dumps(dict(error =  "Sem Dados na porta /dev/serial0"))

    