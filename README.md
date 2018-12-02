# mininet-test

Setup

#!/bin/sh
sudo apt-get update
sudo apt-get -y install git
cd ~
git clone git://github.com/mininet/mininet
mininet_installed=`./mininet/util/install.sh -a|tail`
echo $mininet_installed
sudo apt-get -qqy install net-tools
sudo apt-get -qqy install python-pip gawk python-pyodbc curl

sudo apt-get -qqy install openjdk-8-jre putty
sudo apt-get -qqy  install freetds-bin freetds-dev
pip install numpy

sudo apt-get -qqy install snmp snmpd snmp-mibs-downloader
echo "Downloading MIBs"
echo `sudo download-mibs|wc -l`
mkdir -p ~/.snmp/mibs
sudo sed -i -re 's/([a-z]{2}\.)?#rocommunity/rocommunity/g' /etc/snmp/snmpd.conf
sudo service snmpd restart

#Clone mininet - test
codethere=`ls ~/mininet-test|wc -l`
if [ $codethere -le 0 ]; then
	git clone https://github.com/nabarunjana/mininet-test
	mkdir mininet-test/archive
	chmod 777 mininet-test/*sh  mininet-test/*py
fi

#Install Pycharm
there=`ls ~/pycharm*|wc -l`
if [ $there -le 0 ]; then
	wget https://download-cf.jetbrains.com/python/pycharm-community-2018.1.1.tar.gz 
	echo "Extracting tar file"
	echo `tar -xvzf pycharm-comm* | wc -l`
fi

export PATH=$PATH:`ls -d pycharm*/bin`
chmod 777 ~/pycharm*/bin/*

sudo curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
sudo curl https://packages.microsoft.com/config/ubuntu/16.10/prod.list > /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get -qqy --allow-unauthenticated install msodbcsql
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get -qqy --allow-unauthenticated install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get -qqy install unixodbc-dev

sudo apt-get -qqy install xfce4 xrdp
echo xfce4-session >~/.xsession
sudo service xrdp restart



cd mininet-test
