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
    python power_on.py -h
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

ps aux | grep python
sudo pkill -9 -f 'power_on.py'
sleep 1s

if [ "$ADDR" = "" ]
then
    sudo python power_on.py --simulador=$SIMULADOR --debug=$DEBUG --monitor=$MONITOR --log=$LOG --ignorar=$IGNORAR
else
    sudo python power_on.py --simulador=$SIMULADOR --debug=$DEBUG --monitor=$MONITOR --addr=$ADDR --log=$LOG --ignorar=$IGNORAR
fi

exit