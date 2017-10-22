#!/bin/sh

cd /home/pi/Share/tcc.git/webserver

SIMULADOR=3
DEBUG=0
MONITOR=0
ADDR=""
LOG=1
IGNORAR=0

while getopts hs:d:m:a:i: option
do
 case "${option}"
 in
 h) 
    echo "help start.h"
    echo "-s simulador [0: sem simulador, 1: obdsim, 2: ecu]"
    echo "-d debug [0, 1]"
    echo "-m monitor [0, 1]"
    echo "-l logar em arquivo [0, 1]"
    echo "-a ADDR [MAC ADDR]"
    echo "-i IGNORAR [0,1]"
    python init.py -h
    exit
 ;;
 s) SIMULADOR=${OPTARG};;
 d) DEBUG=${OPTARG};;
 m) MONITOR=${OPTARG};;
 a) ADDR=${OPTARG};;
 i) IGNORAR=${OPTARG};;
 esac
done

echo " "
echo "INICIANDO SERVIDOR..."
echo "SIMULADOR='$SIMULADOR'"
echo "DEBUG='$DEBUG'"
echo "MONITOR='$MONITOR'"
echo "ADDR='$ADDR'"
echo "LOG='$LOG'"
echo "IGNORAR='$IGNORAR'"

ps aux | grep 'init.py'
sleep 1s
sudo pkill -9 -f 'init.py'

if [ "$ADDR" = "" ]
then
    sudo python init.py --simulador=$SIMULADOR --debug=$DEBUG --monitor=$MONITOR --log=$LOG --ignorar=$IGNORAR
else
    sudo python init.py --simulador=$SIMULADOR --debug=$DEBUG --monitor=$MONITOR --addr=$ADDR --log=$LOG --ignorar=$IGNORAR
fi


exit