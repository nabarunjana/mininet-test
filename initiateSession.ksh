#!/usr/bin/env bash
mv IPerf*.zip archive/
zip -m IPerf$(date +%m%d%y.%H%M%S).zip h*.iperf*.dat err.dat ports.txt *Stats.txt h*ping*txt blocked.txt dropped.txt coefficients*txt `ls -rt results*.txt|tail -1` 
echo $(date +%m%d%y%H%M%S) >> log.txt                                  
#sudo python nIperfSessions.py 60 | tee -a log.txt 
echo $1x$2 >> sessionmap.txt
sudo python nIperfSessions.py 100 $1 $2  #2>> errLog.txt
./results.ksh > results$(date +%m%d%y.%H%M%S).txt
echo "Loading to Database"
java -jar monitoring.jar load |tail -1 >> sessionmap.txt
tail -1 coefficients-$1-$2.txt >> sessionmap.txt
