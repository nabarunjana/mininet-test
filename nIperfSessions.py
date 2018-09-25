#!/usr/bin/python

"""
    File name: nIperfSessions.py
    Author: Nabarun Jana
    Date created: 9/12/2017
    Date last modified: 09/15/2018
    Python Version: 2.7
"""

from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel
import sys, threading, time, os, subprocess, re, Properties, pyodbc
from random import *

numNetworks = 2
hostPerSw = 16  # 8
select_rand_hosts = 2  # true = 1
different_subnets = 0  # false = 0
interval = 2  # seconds
duration = int(sys.argv[2])  # 20 seconds
CLIon = 0  # 0 = Off (No CLI)
test_with_data = 1
monitoring = 1
mesh = 1  # 1 = Mesh network
no_time_run = 2
switchLevels = 10  # 5
throughput = int(sys.argv[3])  # 8 Mbps
skip_coeff = 0
blocked = 0
dropped = 0
test = 'iperf'
dateCmd = "date +%H:%M:%S"
slaDel = 200
slaBW = 1000000
bandwidth = 64  # MBits/sec
session = sys.argv[2] + "x" + sys.argv[3]
controllerIP = '127.0.0.1'

if CLIon == 1:
    test_with_data = 0
    monitoring = 0


class MyTopo(Topo):
    """Tree topology of k switches, with num_sws host per switch."""

    def __init__(self, num_sws=2, **opts):

        super(MyTopo, self).__init__(**opts)

        # self.num_sws = num_sws
        last_router = None
        routers = []
        for netNum in irange(1, numNetworks):
            central_switch = self.addSwitch('s%s0' % netNum, cls=OVSKernelSwitch)
            rtr_ip_add = '10.0.0.%s' % (255 - netNum) if different_subnets == 0 else '10.0.%s.254' % netNum
            central_router = self.addSwitch('r%s0' % netNum, cls=OVSKernelSwitch, ip=rtr_ip_add)
            dig = get_digits(num_sws * hostPerSw)
            for sw_num in range(num_sws):
                switch = self.addSwitch('s%s%s' % (netNum, sw_num+1), cls=OVSKernelSwitch)
                self.addLink(switch, central_switch, bw=bandwidth)
                for host_num in irange(1, hostPerSw):
                    dev_num = hostPerSw * sw_num + host_num
                    ip_add = "10.0.%s.%s" % ((netNum - 1), dev_num)
                    ip_add += "/16" if different_subnets == 0 else "/24"
                    host = self.addHost('h%s%s' % (netNum, pad(dev_num,dig)), ip=ip_add, defaultRoute="via "+rtr_ip_add)
                    self.addLink(host, switch, bw=bandwidth)

            self.addLink(central_switch, central_router, bw=bandwidth)
            if last_router:
                if mesh == 1:
                    for previousRouter in routers:
                        self.addLink(previousRouter, central_router, bw=bandwidth)
                else:
                    self.addLink(central_router, last_router, bw=bandwidth)
            last_router = central_router
            routers.append(last_router)


# function to perform iperf on 2 hosts

def pad(num, dig):
    num = str(num)
    while len(num) < dig:
        num = "0" + num
    return num


def get_digits(num):
    dig = 0
    while num > 0:
        num /= 10
        dig += 1
    return dig


def read_last_line(filename):
    read_file = open(filename, 'r')
    lines = read_file.readlines()
    read_file.close()
    return lines[len(lines) - 1]


def read_coeff():
    coeffile = ('coefficients-%s-%s.txt' % (sys.argv[2], sys.argv[3]))
    coeff = read_last_line(coeffile)
    return float(re.sub("[^0-9.]", "", coeff))


class DataTraffic:

    def __init__(self):
        pass

    def perform_iperf(self, net, i):
        # Popping out 2 hosts, one for client the other as server
        hosts = net.hosts
        if select_rand_hosts == 1:
            h1, h2 = hosts.pop(int(random() * len(hosts))), hosts.pop(
                int(random() * len(hosts)))  # ---- selecting hosts at random
        elif numNetworks == 1:
            i += 1
            h1, h2 = net.get('h%s%s' % (1, 2 * i - 1)), net.get(
                'h%s%s' % (1, 2 * i))  # hosts.pop(0),hosts.pop(0) #len(hosts)/2)
        elif select_rand_hosts == 2:
            h1, h2 = hosts.pop(randrange(0, len(hosts)/2-1)), hosts.pop(randrange(len(hosts) / 2 + 1, len(hosts)))
        else:  # selecting corresponding hosts from the 1st and last then sequential 2nd and 2nd last subnet and so on
            max_hosts = hostPerSw * switchLevels
            next_subnet = int(i / max_hosts)
            h1, h2 = net.get('h%s%s' % (1 + next_subnet, pad(i % max_hosts + 1, get_digits(max_hosts)))), net.get(
                'h%s%s' % (numNetworks - next_subnet, pad(i % max_hosts + 1, get_digits(max_hosts))))
        # -------- removed 'h%s' %(i+1), 'h%s' %(i+7)) #'h%s' %(round(random()*15)), 'h%s' %(round(random()*15)) )
        # ----- replaced with list.pop() -------- removed net.iperf( (h1, h4) )  ---- replacesd with host.cmd()
        print "Performing Iperf test between", h1, h1.IP(), "(c) and ", h2, h2.IP(), "(s)"
        h2.cmd('%s -s &' % test)  # running iperf server in the background (&)
        global throughput, dropped, blocked  # Since value being changed
        if throughput == 0:
            throughput = int(h2.name[1:]) * int(h1.name[1:]) / 10000
        if (skip_coeff == 1) | (random() < read_coeff()):		# Condition to generatte new flow
            bw_file = '%s-%s.%s.dat' % (h1, h2, test)
            h1.cmd('ping %s &' % h2.IP())						# Learn path and wait for response to reach
            time.sleep(10)
            h1.cmd('ping %s -i %s -w %s | gawk \'{ print strftime("%s"), $0 }\' >> %s-%s.ping.txt 2>> err.dat &' % (
                h2.IP(), interval / 2, duration, "%H:%M:%S", h1, h2))
            h1.cmd('%s -c %s -b %sM -i %s -t %s | gawk \'{ print strftime("%s"), $0 }\' >> %s 2>> err.dat' % (
                test, h2.IP(), throughput, interval / 2, duration, "%H:%M:%S",
                bw_file))  # running iperf client in background until complete (&&)
            coefficient = read_coeff()
            if no_time_run == 1:
                bw_file = open(bw_file, 'r')
                bw_line = bw_file.readlines()
                if len(bw_line) == 0:
                    dropped += 1
                else:
                    line = bw_line[len(bw_line) - 1].replace('  ', ' ')
                    pad_num_chars = 1 if len(line.split(' ')) == 10 else 0
                    bw = float(line.split(' ')[7+pad_num_chars])
                    bw_unit = line.split(' ')[8+pad_num_chars]
                    mx = {'G': 1000000000, 'M': 1000000, 'K': 1000}
                    multiplier = mx.get(bw_unit[0], 1)
                    del_file = '%s-%s.ping.txt' % (h1, h2)
                    del_line = read_last_line(del_file)
                    delay = float(del_line.replace(' +', ' ').split(' ')[4].split("/")[1])
                    if (bw * multiplier > slaBW) & (delay < slaDel):
                        coefficient *= 1.1
                        if coefficient > 1:
                            coefficient = 1
                    else:
                        coefficient *= 0.9

        else:
            blocked += 1
            coefficient = read_coeff()

        append_file('coefficients-%s-%s.txt' % (sys.argv[2], sys.argv[3]), coefficient)
        # h2.sendInt()
        hosts.append(h1)
        hosts.append(h2)


def print_file(filename, val):
    wrfile = open(filename, 'w')
    wrfile.write(str(val))
    wrfile.close()


def append_file(filename, val):
    wrfile = open(filename, 'a')
    wrfile.write(str(val) + "\n")
    wrfile.close()


def get_coeff():
    p = Properties.Properties()
    p.load('dbcon.properties')
    conn = pyodbc.connect(DRIVER='{ODBC Driver 13 for SQL Server}', server=p.getProperty("host"),
                          user=p.getProperty("user"), password=p.getProperty("password"),
                          database=p.getProperty("database"))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT avg(coeff) FROM vCoefficients WHERE BATCH_ID in (select BATCH_ID from sessionMap where toUse like "
        "'SRandPairs1%s' and slaBW=%s and slaDel=%s and bandwidth=%s and session='%s');" % (
            '%1000%', slaBW, slaDel, bandwidth, session))
    row = str(cursor.fetchone()).strip('(, )')
    if row == "None":
        row = "1"
    print(row)
    conn.close()
    return float(re.sub("[^0-9.]", "", row))


def simple_test():
    """Create and test a simple network"""
    topo = MyTopo(num_sws=switchLevels)
    net = Mininet(topo, link=TCLink, switch=OVSKernelSwitch, autoSetMacs=True, autoStaticArp=False,
                  controller=lambda name: RemoteController(name, ip=controllerIP, port=6633))
    net.start()

    if monitoring == 1:
        # --- Monitoring
        os.popen('ip link show > ports.txt')
        # '''
        snmp_dev_proc = subprocess.Popen(
            'while sleep %s; do %s; snmpwalk -v 1 -c public -O e localhost 1.3.6.1.2.1.25.2.3.1.6.1;'
            ' snmpwalk -v 1 -c public -O e localhost 1.3.6.1.2.1.25.3.3.1.2; done>> DevStats.txt 2>> err.txt &'
            % (interval, dateCmd), shell=True)

        c0 = net.get('c0')
        c0.cmd('snmpd -Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid -c /etc/snmp/snmpd.conf')
        snmp_con_proc = c0.cmd(
            'while sleep %s; do %s; snmpwalk -v 1 -c public -O e %s 1.3.6.1.2.1.25.2.3.1.6.1;'
            ' snmpwalk -v 1 -c public -O e %s 1.3.6.1.2.1.25.3.3.1.2; done>> ControllerStats.txt 2>> err.txt &'
            % (interval, dateCmd, controllerIP, controllerIP))

        for r in irange(1, numNetworks):
            router = net.get('r%s0' % r)
            router.cmd('snmpd -Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid -c /etc/snmp/snmpd.conf')
            router.cmd(
                'while sleep %s; do %s; snmpwalk -v 1 -c public -O e %s 1.3.6.1.2.1.2.2.1.16; '
                'done>> Router%sIfOutStats.txt 2>> err.txt &' % (
                     interval, dateCmd, router.IP(), r))  # .1.3.6.1.2.1.2.2.1.16
        # '''

    # net.staticArp()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)

    if CLIon == 1:
        CLI(net)

    # os.system('echo \"1\">>coefficients-%s-%s.txt' % (sys.argv[2], sys.argv[3]))
    if no_time_run == 2:
        coefficient = get_coeff()
    else:
        coefficient = 1
    append_file('coefficients-%s-%s.txt' % (sys.argv[2], sys.argv[3]), coefficient)
    start_time = time.time()
    # ------- removed net.pingAll()   ----- replaced with net.staticArp()
    # ------- removed    CLI( net )
    n = int(sys.argv[1])  # getting number of IPerf tests from command line

    ''' ---- Removed 02-01-2018 ---- Invalid after hosts.append()
    hpairs = len(net.hosts)/2
    if n > hpairs:
        print "Number of IPerf tests exceeds host pairs. Reducings tests from %s to %s"  %(n,hpairs)
        n = hpairs
    else:
        print "Number of IPerf tests %s" %n
    '''

    if test_with_data == 1:
        threads = []
        t = {}
        # Creating n threads, one for each iperf session
        for i in range(int(n)):
            dt = DataTraffic()
            t[i] = threading.Thread(target=DataTraffic.perform_iperf, args=(dt, net, i))
            t[i].daemon = True
            t[i].start()
            threads.append(t[i])
            time.sleep(interval)
        # ----- removed time.sleep(20) ------ replaced with join()

        # Making the current thread wait for all the created threads to complete
        for i in range(int(n)):
            t[i].join()

        c0.sendInt()
        for r in irange(1, numNetworks):
            router = net.get('r%s0' % r)
            router.sendInt()
    net.stop()
    if monitoring == 1:
        snmp_dev_proc.kill()
    # os.kill(int(snmp_con_proc.split()[1]), signal.CTRL_C_EVENT)

    stop_time = time.time()
    print_file('blocked.txt', blocked)
    print_file('dropped.txt', dropped)
    print(stop_time - start_time)
    print os.system('%s >> log.txt; echo %s >> log.txt' % (
          dateCmd, stop_time - start_time))  # dummy command to print  seconds of the clock


if __name__ == '__main__':
    # Tell mininet to print only output
    setLogLevel('output')
    open('dbcon.properties', 'r')
    try:
        simple_test()
    except:
        cleanup()
        simple_test()

topos = {'mytopo': (lambda: MyTopo())}