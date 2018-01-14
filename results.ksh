#!/usr/bin/env bash
for file in `ls -rt h*iperf.dat`
do
	echo `echo $file|cut -d"." -f1` `cat $file | tail -1 | cut -d" " -f8-`
done

for file in `ls -rt h*iperf3.dat`
do
	echo `echo $file| cut -d"." -f1` `cat $file | grep receiver | cut -d" " -f6-`
done