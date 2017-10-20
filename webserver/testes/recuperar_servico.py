import bluetooth, getopt, sys

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ac:c:",["addr=", "com="])
    except getopt.GetoptError:
        print('recuperar_servico.py --addr=[addr] --com=[numCom]')
        sys.exit(2)
    
    com = None
    for opt, arg in opts:
        if opt in ("-a", "--addr"):
            addr = str(arg)
        if opt in ("-c", "--com"):
            com = str(arg)
    
    if com is None: 
        com = str(-1)

    services = bluetooth.find_service(address=addr)

    if len(services) > 0:
        for svc in services:
            if(svc["protocol"] == "RFCOMM"):
                if(svc["name"] == "COM" + com):
                    print(svc["port"])
                if(svc["name"] == "BLT"):
                    print(svc["port"])

    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])