#!/usr/bin/env bash
mv IPerf*.zip archive/
zip -m IPerf$(date +%m%d%y.%H%M%S).zip h*.iperf*.dat err.dat ports.txt *Stats.txt h*ping*txt `ls -rt results*.txt|tail -1` 
echo $(date +%m%d%y%H%M%S) >> log.txt                                  
#sudo python nIperfSessions.py 60 | tee -a log.txt 
sudo python nIperfSessions.py 4 #2>> errLog.txt
./results.ksh > results$(date +%m%d%y.%H%M%S).txt
java -jar monitoring.jar