#!/usr/bin/env bash

./initiateSession.ksh 16 32 1
./initiateSession.ksh 8 32 1
./initiateSession.ksh 8 64 1
./initiateSession.ksh 16 64 1
toUse="'SRandPairs1x1000'" #`date +%d%m%y` #"'2SW10sL64C100x1'" #
skip=`grep 'skipcoeff' nIperfSessions.py |head -1 | cut -d '=' -f2`
if [ $skip == 1 ]; then slaDel=0; slaBW=0; else
slaDel=` grep 'slaDel' nIperfSessions.py |head -1 | cut -d '=' -f2`
slaBW=`grep 'slaBW' nIperfSessions.py |head -1 | cut -d '=' -f2`
fi
bandwidth=`grep 'bandwidth' nIperfSessions.py|head -1|gawk '{print $3}'`
cat sessionmap.txt|while read line; do
	s=\'$line\'; read line2; b=$line2;read line3; c=$line3;
	java -jar monitoring.jar insert sessionMap $b $s $toUse $c $slaDel $slaBW $bandwidth;
done
mv sessionmap.txt 'sessionmap'$toUse'.txt'

./initiateSession.ksh 16 32 2
./initiateSession.ksh 8 32 2
./initiateSession.ksh 8 64 2
./initiateSession.ksh 16 64 2
toUse="'SRandPairs2x1000'" #`date +%d%m%y` #"'2SW10sL64C100x1'" #
skip=`grep 'skipcoeff' nIperfSessions.py |head -1 | cut -d '=' -f2`
if [ $skip == 1 ]; then slaDel=0; slaBW=0; else
slaDel=` grep 'slaDel' nIperfSessions.py |head -1 | cut -d '=' -f2`
slaBW=`grep 'slaBW' nIperfSessions.py |head -1 | cut -d '=' -f2`
fi
bandwidth=`grep 'bandwidth' nIperfSessions.py|head -1|gawk '{print $3}'`
cat sessionmap.txt|while read line; do
	s=\'$line\'; read line2; b=$line2;read line3; c=$line3;
	java -jar monitoring.jar insert sessionMap $b $s $toUse $c $slaDel $slaBW $bandwidth;
done
mv sessionmap.txt 'sessionmap'$toUse'.txt'