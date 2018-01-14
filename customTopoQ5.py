#!/usr/bin/env python
"""
CustomHomework.py - Homework to create custom topology with link parameters 
"""
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel

class NetworkOfNetworks(Topo):
	def __init__(self, **opts):
		Topo.__init__(self, **opts)
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')
		h5 = self.addHost('h5')
		h6 = self.addHost('h6')
		h7 = self.addHost('h7')
		h8 = self.addHost('h8')
		h9 = self.addHost('h9')
		h10 = self.addHost('h10')
		h11 = self.addHost('h11')
		h12 = self.addHost('h12')
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')

#Add the links between the switches and the hosts by referring to the topology above
		self.addLink(s1, s2,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s2, s3,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s3, s4,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s4, s5,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		                   
		self.addLink(s1, h1,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s1, h2,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s1, h3,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		                   
		self.addLink(s2, h4,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s2, h5,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		                   
		self.addLink(s3, h6,bw=15,delay='5ms',loss=1,max_queue_size=1000) 
		self.addLink(s3, h7,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		
		self.addLink(s4, h8,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s4, h9,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		
		self.addLink(s5, h10,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s5, h11,bw=15,delay='5ms',loss=1,max_queue_size=1000)
		self.addLink(s5, h12,bw=15,delay='5ms',loss=1,max_queue_size=1000)

#Continue adding the other links

	if __name__ == '__main__':
    		setLogLevel( 'info' )

# Create data network
topo = NetworkOfNetworks()
net = Mininet(topo=topo, link=TCLink, autoSetMacs=True,
           autoStaticArp=True)

# Run network
net.start()
CLI( net )
net.stop()
