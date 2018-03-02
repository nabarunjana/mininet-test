#!/usr/bin/python

'''
	File name: nIperfSessions.py
	Author: Nabarun Jana
	Date created: 9/12/2017
	Date last modified: 02/28/2018
	Python Version: 2.7
'''

from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController,OVSKernelSwitch
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
import sys,threading,time,os,subprocess,signal,re, numpy
from random import *

numNetworks = 2
hostsPerSwitch = 8					#8
selectRandomHosts =1				# true = 1
differentSubnets = 0				# false = 0
interval = 10						# seconds
duration = int(sys.argv[2])			# 20 seconds
CLIon = 0							# 0 = Off (No CLI)
mesh = 1							# 1 = Mesh network
switchLevels = 5					#5
throughput = int(sys.argv[3])		# 8 Mbps
test = 'iperf'
dateCmd = "date +%H:%M:%S"
class MyTopo(Topo):
	"Star topology of k switches, with 4 host per switch."

	def __init__(self, k=2, **opts):
		"""Init.
		k: number of switches 
		hconf: host configuration options
		lconf: link configuration options"""
		
		#----- removed print "This is the name of the script: ", sys.argv[0]
		super(MyTopo, self).__init__(**opts)
		
		self.k = k
		bandwidth=100 #MBits/sec
		#------ removed lastSwitch = None
		lastRouter = None
		routers = []
		for r in irange(1,numNetworks):
			centralSwitch = self.addSwitch('s%s0' %(r))
			if differentSubnets == 0:
				centralRouter = self.addSwitch('r%s0' %(r),ip='10.0.0.%s' %(255-r))
			else:
				centralRouter = self.addSwitch('r%s0' %(r),ip='10.0.%s.254' %r)
			for i in irange(0, k-1):
				switch = self.addSwitch('s%s%s' % (r,i+1))
				self.addLink(switch,centralSwitch ,bw=bandwidth)
				for j in range(1,(hostsPerSwitch+1)):
					if differentSubnets == 0:
						host = self.addHost('h%s%s' % (r,hostsPerSwitch*i+j), Mask='255.255.0.0') 		# ,ip="10.0.0.%s/24" %((r-1)*k*hostsPerSwitch + hostsPerSwitch*i+j)) # % (r,(hostsPerSwitch*i+j)), defaultRoute = "via 10.0.%s.254" % (r) )
					else:
						host = self.addHost('h%s%s' % (r,hostsPerSwitch*i+j) ,ip="10.0.%s.%s/24" %((r-1),hostsPerSwitch*i+j), defaultRoute ="via 10.0.%s.254" %r) # % (r,(hostsPerSwitch*i+j)), defaultRoute = "via 10.0.%s.254" % (r) )
					self.addLink( host, switch ,bw=bandwidth)
				#""" -------removed 
			self.addLink( centralSwitch, centralRouter ,bw=bandwidth)
			if lastRouter:
				if mesh ==1:
					for previosRouter in routers:
						self.addLink(previosRouter,centralRouter,bw=bandwidth)
				else:
					self.addLink( centralRouter, lastRouter ,bw=bandwidth)
			lastRouter = centralRouter
			routers.append(lastRouter)
#function to perform iperf on 2 hosts			
def performIperf(net,i):
	#Popping out 2 hosts, one for client the other as server
	hosts = net.hosts
	if selectRandomHosts == 1:
		h1, h2 = hosts.pop(int(random()*len(hosts))),hosts.pop(int(random()*len(hosts))) #---- selecting hosts at random
	elif numNetworks==1:
		i+=1
		h1, h2 = net.get('h%s%s' %(1,2*i-1)), net.get('h%s%s' %(1,2*i)) #hosts.pop(0),hosts.pop(0) #len(hosts)/2)
	else:			#selecting corresponding hosts from the 1st and last then sequential 2nd and 2nd last subnet and so on
		maxHosts = hostsPerSwitch*switchLevels
		nextSubnet=int(i/maxHosts)
		h1, h2 = net.get('h%s%s' %(1+nextSubnet,i%maxHosts+1)), net.get('h%s%s' %(numNetworks-nextSubnet,i%maxHosts+1))
	#-------- removed 'h%s' %(i+1), 'h%s' %(i+7)) #'h%s' %(round(random()*15)), 'h%s' %(round(random()*15)) ) ----- replaced with list.pop()
	#-------- removed net.iperf( (h1, h4) )  ---- replacesd with host.cmd()
	print "Performing Iperf test between", h1, h1.IP(), "(c) and ", h2, h2.IP(), "(s)"
	h2.cmd('%s -s &' %(test)) #running iperf server in the background (&)
	global throughput		# Since value being changed
	if throughput == 0:
		throughput = int(h2.name[1:])*int(h1.name[1:])/10000
	
	#coefficient=float(h1.cmd('cat coefficients-%s-%s.txt|tail -1' %(sys.argv[2],sys.argv[3])).rstrip())
	#coeff=h1.cmd('cat coefficients-%s-%s.txt|tail -1' %(sys.argv[2],sys.argv[3]))
	coeffile=('coefficients-%s-%s.txt' %(sys.argv[2],sys.argv[3]))
	coeffile = open(coeffile,'r')
	lines=coeffile.readlines()
	coeff = lines[len(lines)-1]
	coefficient = float(re.sub("[^0-9.]", "", coeff))
	fcoeff=0
	if random() < coefficient:
		filename = '%s-%s.%s.dat' % (h1, h2, test)
		h1.cmd('ping %s -i %s -w %s | gawk \'{ print strftime("%s"), $0 }\' >> %s-%s.ping.txt 2>> err.dat &' %(h2.IP(),interval/2,duration,"%H:%M:%S",h1,h2))
		h1.cmd('%s -c %s -b %sM -i %s -t %s | gawk \'{ print strftime("%s"), $0 }\' >> %s 2>> err.dat &&' %(test,h2.IP(),throughput,interval/2,duration,"%H:%M:%S",filename)) #running iperf client in background until complete (&&)
		bwfile = open(filename, 'r')
		bwline = bwfile.readlines()
		line = bwline[len(bwline) - 1]
		i=0
		if len(re.split('\s+', line))==11:
			i=1
		bw = float(re.split('\s+', line)[7+i])
		bwUnit = re.split('\s+', line)[8+i]
		multiplier = 1
		if bwUnit[0] == 'K':
			multiplier = 1000
		elif bwUnit[0] == 'M':
			multiplier = 1000000
		elif bwUnit[0] == 'G':
			multiplier = 1000000000
		delfile = ('%s-%s.ping.txt' %(h1, h2))
		delfile = open(delfile,'r')
		delline= delfile.readlines()
		line = delline[len(delline) - 1]
		print line
		delay = float(re.split('/+', line)[4])
		coeffile=('coefficients-%s-%s.txt' %(sys.argv[2],sys.argv[3]))
		coeffile = open(coeffile, 'r')
		lines = coeffile.readlines()
		coeff = lines[len(lines) - 1]
		coefficient = float(re.sub("[^0-9.]", "", coeff))
		if ((bw * multiplier > 1000000) & (delay < 100)):
			fcoeff = 1.1 * coefficient
			if fcoeff > 1: fcoeff = 1
		else:
			fcoeff = 0.9 * coefficient
		#print bw

	else:
		fcoeff=1*coefficient
	
	h1.cmd('echo %s >>coefficients-%s-%s.txt' %(fcoeff,sys.argv[2],sys.argv[3]))
	h2.sendInt()
		
	hosts.append(h1)
	hosts.append(h2)
	#-------- temp tried -- &&' %(test,h2.IP(),duration,"date +**%H:%M:%S"))#
	
def simpleTest():
	"Create and test a simple network"
	topo = MyTopo(k=switchLevels)
	net = Mininet(topo, link=TCLink , autoSetMacs=True,
           autoStaticArp=False, controller=lambda name: RemoteController( name, defaultIP='127.0.0.1', port =6633 ))
	net.start()
	
	#--- Monitoring 
	os.popen('ip link show > ports.txt')
	snmpDevProc = subprocess.Popen('while sleep %s; do %s; snmpwalk -v 1 -c public -O e localhost hrStorageUsed.1; snmpwalk -v 1 -c public -O e localhost hrProcessorLoad; done>> DevStats.txt 2>> err.txt &' %(interval,dateCmd), shell=True)
	
	c0= net.get('c0')
	c0.cmd('snmpd -Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid -c /etc/snmp/snmpd.conf')
	snmpConProc = c0.cmd('while sleep %s; do %s; snmpwalk -v 1 -c public -O e localhost hrStorageUsed.1; snmpwalk -v 1 -c public -O e localhost hrProcessorLoad; done>> ControllerStats.txt 2>> err.txt &' %(interval,dateCmd))
	
	for r in irange(1,numNetworks):
		router = net.get('r%s0' %(r))
		router.cmd('snmpd -Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid -c /etc/snmp/snmpd.conf')
		router.cmd('while sleep %s; do %s; snmpwalk -v 1 -c public -O e %s ifOutOctets; done>> Router%sIfOutStats.txt 2>> err.txt &' %(interval,dateCmd,router.IP(),r))		#.1.3.6.1.2.1.2.2.1.16
		
	#net.staticArp()
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	
	if CLIon == 1:
		CLI( net )
		
	os.system('echo \"1\">>coefficients-%s-%s.txt' %(sys.argv[2],sys.argv[3]))	
	startTime = time.time()	
	print "Testing network connectivity"
	#------- removed net.pingAll()   ----- replaced with net.staticArp()
	#------- removed    CLI( net ) 
	n = int(sys.argv[1])  # getting number of IPerf tests from command line
	#"""
	threads = []
	t={}
	
	#net.get('h11').cmd('while sleep %s; do %s;ping -c 1 10.0.0.16|grep avg ; done >> h1ping2.txt 2>> err.txt &' %(interval/2,dateCmd))
	
	''' ---- Removed 02-01-2018 ---- Invalid after hosts.append()
	hpairs = len(net.hosts)/2
	if n > hpairs:
		print "Number of IPerf tests exceeds host pairs. Reducings tests from %s to %s"  %(n,hpairs)
		n = hpairs
	else:
		print "Number of IPerf tests %s" %n
	'''	
		
	#Creating n threads, one for each iperf session
	for i in range(int(n)):
		t[i] = threading.Thread(target=performIperf, args=(net,i,))
		threads.append(t[i])
	
		time.sleep(interval)
		t[i].daemon = True
		t[i].start()
	#----- removed time.sleep(20) ------ replaced with join()
	
	#Making the current thread wait for all the created threads to complete
	for i in range(int(n)):
		t[i].join() 
		#"""
	c0.sendInt()
	for r in irange(1,numNetworks):
		router = net.get('r%s0' %(r))
		router.sendInt()
	net.stop()
	snmpDevProc.kill()
	#os.kill(int(snmpConProc.split()[1]), signal.CTRL_C_EVENT)
	
	#for i in range(int(n)):
		#t[i].notify() 
	stopTime = time.time()
	print(stopTime-startTime)
	print os.system('%s >> log.txt; echo %s >> log.txt' %(dateCmd,stopTime-startTime))		#dummy command to print  seconds of the clock
	
if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	try:	simpleTest()
	except: 
		cleanup()
		simpleTest()
		
topos = { 'mytopo': ( lambda: MyTopo() ) }