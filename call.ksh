#!/usr/bin/env bash
./initiateSession.ksh 40 8
./initiateSession.ksh 80 4
./initiateSession.ksh 80 8
./initiateSession.ksh 160 4
./initiateSession.ksh 160 2
./initiateSession.ksh 160 8
./initiateSession.ksh 40 16
./initiateSession.ksh 80 16
toUse="'Wait10sL64NoCoeff100x1'" #`date +%d%m%y`
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

#!/usr/bin/env bash
./initiateSession.ksh 40 8
./initiateSession.ksh 80 4
./initiateSession.ksh 80 8
./initiateSession.ksh 160 4
./initiateSession.ksh 160 2
./initiateSession.ksh 160 8
./initiateSession.ksh 40 16
./initiateSession.ksh 80 16
toUse="'Wait10sL64NoCoeff100x2'" #`date +%d%m%y`
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

#!/usr/bin/env bash
./initiateSession.ksh 40 8
./initiateSession.ksh 80 4
./initiateSession.ksh 80 8
./initiateSession.ksh 160 4
./initiateSession.ksh 160 2
./initiateSession.ksh 160 8
./initiateSession.ksh 40 16
./initiateSession.ksh 80 16
toUse="'Wait10sL64NoCoeff100x3'" #`date +%d%m%y`
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