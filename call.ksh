#!/usr/bin/env bash

for i in {0..2}; do 
./initiateSession.ksh 1 512 $i
./initiateSession.ksh 1 256 $i
./initiateSession.ksh 2 256 $i
./initiateSession.ksh 256 1 $i
./initiateSession.ksh 256 2 $i
./initiateSession.ksh 512 1 $i
toUse="'Extreme"$i"x1000'" 
skip=`grep 'skip_coeff' nIperfSessions.py |head -1 | cut -d '=' -f2`
if [ $skip==1 ]; then slaDel=0; slaBW=0; else
slaDel=` grep 'slaDel' nIperfSessions.py |head -1 | cut -d '=' -f2`
slaBW=`grep 'slaBW' nIperfSessions.py |head -1 | cut -d '=' -f2`
fi
bandwidth=`grep 'bandwidth' nIperfSessions.py|head -1|gawk '{print $3}'`
cat sessionmap.txt|while read line; do
	s=\'$line\'; read line2; b=$line2;read line3; c=$line3;
	java -jar monitoring.jar insert sessionMap $b $s $toUse $c $slaDel $slaBW $bandwidth;
done
mv sessionmap.txt 'sessionmap'$toUse'.txt'
done