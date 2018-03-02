#!/usr/bin/env bash
./initiateSession.ksh 20 8
./initiateSession.ksh 40 4
./initiateSession.ksh 40 8
./initiateSession.ksh 80 4
./initiateSession.ksh 80 8
./initiateSession.ksh 160 4
./initiateSession.ksh 160 2
./initiateSession.ksh 160 8
./initiateSession.ksh 20 16
./initiateSession.ksh 40 16
./initiateSession.ksh 80 16
cat sessionmap.txt|while read line; do s=\'$line\'; read line2; b=$line2;read line3; c=$line3;
java -jar monitoring.jar insert sessionMap $b $s `date +%d%m%y` $c;
done
