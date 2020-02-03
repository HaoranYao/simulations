from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Switch 
from mininet.cli import CLI 
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.node import NullController
from mininet.node import Switch
from mininet.nodelib import LinuxBridge
import os
import time

class MySwitch(Switch):
    def start(self, controllers):
        pass


class Phase1_topo( Topo ):
        
    def __init__ ( self ):
        

        Topo.__init__(self)


        h1=self.addHost('h1',ip='10.220.0.5/24', defaultRoute='via 10.220.0.1')
        h2=self.addHost('h2',ip='10.221.0.5/24', defaultRoute='via 10.221.0.1')
        h3=self.addHost('h3',ip='10.221.0.6/24', defaultRoute='via 10.221.0.1')
        h4=self.addHost('h4',ip='10.221.0.7/24', defaultRoute='via 10.221.0.1')
        h5=self.addHost('h5',ip='10.221.0.8/24', defaultRoute='via 10.221.0.1')

        #sw2=self.addSwitch('s2')
        sw1=self.addSwitch('s1', cls = MySwitch)
        sw2=self.addSwitch('s2', cls = LinuxBridge)
        sw3=self.addSwitch('s3', cls = LinuxBridge)

    #    sw1.setIP('100.0.0.2/24',intf='s1-eth2')
        
        self.addLink(h1,sw1)
        self.addLink(sw1,sw2)
        self.addLink(h2,sw2)
        self.addLink(h3,sw2)
        self.addLink(h4,sw2)
        self.addLink(h5,sw2)

        self.addLink(h2,sw3)
        self.addLink(h3,sw3)
        self.addLink(h4,sw3)
        self.addLink(h5,sw3)
        self.addLink(sw1,sw3)
        
topology = {'topology' : (lambda : topo () )}
if __name__ == "__main__":
    topo= Phase1_topo()
    #ctrl=RemoteController ("c0" , ip= "127.0.0.1" , port=6633)


    net=Mininet(
                topo            =   topo,
                #switch          =   MySwitch,
                controller      =   NullController,
                autoSetMacs     =   True,
                autoStaticArp   =   True,
                build           =   True,
                cleanup         =   True
                )
    net.start()
    s1 = net.get('s1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')

    h2.intf('h2-eth1').setIP('192.168.0.5/24')
    h3.intf('h3-eth1').setIP('192.168.0.6/24')
    h4.intf('h4-eth1').setIP('192.168.0.7/24')
    h5.intf('h5-eth1').setIP('192.168.0.8/24')


    
    s1.intf('s1-eth1').setIP('10.220.0.1/24')
    s1.intf('s1-eth2').setIP('10.221.0.1/24')
    s1.intf('s1-eth1').setMAC('92:08:01:87:04:6d')
    s1.intf('s1-eth2').setMAC('6e:e9:dc:f5:3d:5b')
    s1.intf('s1-eth3').setIP('192.168.0.1/24')
    h2.cmd('python -m http.server 80 &')
    h3.cmd('python -m http.server 80 &')
    h4.cmd('python -m http.server 80 &')
    h5.cmd('python -m http.server 80 &')
    # h2.cmd('python server.py 0 &')
    # h3.cmd('python server.py 1 &')
    # h4.cmd('python server.py 2 &')
    # h5.cmd('python server.py 3 &')
    CLI(net)
    
 
    
