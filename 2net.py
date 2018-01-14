#!/usr/bin/env python
"""
CustomHomework.py - Homework to create custom topology with link parameters 
"""
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel

class NetworkOfNetworks(Topo):
	def __init__(self, **opts):
		Topo.__init__(self, **opts)
		h1 = self.addHost('h1', ip='10.0.1.2',defaultRoute='via 10.0.1.1')
		h2 = self.addHost('h2', ip='10.0.2.2',defaultRoute='via 10.0.2.1')
		s1 = self.addSwitch('s1', ip='10.0.1.1')
		s2 = self.addSwitch('s2', ip='10.0.2.1')

#Add the links between the switches and the hosts by referring to the topology above		                 
		self.addLink(s1, h1)
		self.addLink(s2, h2)
		self.addLink(s1, s2)
		
#Continue adding the other links

	if __name__ == '__main__':
    		setLogLevel( 'info' )

# Create data network
topo = NetworkOfNetworks()
net = Mininet(topo=topo, link=TCLink, autoSetMacs=True,
           autoStaticArp=False, controller=lambda name: RemoteController( name, defaultIP='127.0.0.1', port =6633 ))

# Run network
net.start()
CLI( net )
net.stop()

topos = { 'mytopo': ( lambda: NetworkOfNetworks() ) }
