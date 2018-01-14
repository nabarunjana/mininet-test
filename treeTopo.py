#!/usr/bin/python

"Create a 64-node tree network, and test connectivity using ping."


from mininet.log import setLogLevel, info
from mininet.topolib import TreeNet
import sys

def treePing():
	"Run ping test on 64-node tree networks."
	# To run this code type 'sudo python script_name.py depth fanout'
	# where script_name.py is the name you save the script and fanout
	# being the number corresponding to the depth and fanout required
	depth = int(sys.argv[1])
	fanout = int(sys.argv[2])
	network = TreeNet( depth=depth, fanout=fanout)
	network.start()
	network.staticArp()
	hosts = network.hosts
	h1 = hosts[0]
	outputFile = 'pingresults-%s-%s.txt' %(depth,fanout)
	h1.cmd('date +%m%d%y.%H%M%S > ' + outputFile ) # cmd used to specify
	# the command to execute within the hosts terminal 9in the background)
	for i in range(len(hosts)-1):
		h2 = hosts.pop(1) # get the host at index =0 (note h1 is at index 0)
		info('%s ping %s \n' %(h1,h2)) # %s being replaced with the data
		# passed in the brackets i.e. h1 and h2 in this case
		h1.cmd('ping -c20 %s >> %s 2>> errPing.dat &&' %(h2.IP(),outputFile)) #-c specifies
	#  number of times to ping
	results = h1.cmd("cat %s|grep avg | cut -d \" \" -f4,5|awk -F '[/ ]'"
					 " '{print $4\" \"$5}' | tee avgResults-%s-%s.txt" %(outputFile,depth,fanout))
	network.stop()
	print 'Average RTTs are \n', results

if __name__ == '__main__':
    setLogLevel( 'info' )
    treePing()