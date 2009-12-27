from pythonwifi.iwlibs import Wireless
from iocapture import IOCapture

class WifiLoc(object):

  def __init__(self, interface):
    self.interface = interface

    self.known_networks = {}
    self.w = Wireless(self.interface)

  def update_location(self):
    IOCapture.startCapture()
    networks = []

    try:
      networks = self.w.scan()
    finally:
      IOCapture.stopCapture()

    for network in networks:
      if not network.bssid in self.known_networks:
        self.known_networks[network.bssid] = network

    self.reachable_networks = networks
    
  def getCurrentAP(self):

    networks = self.reachable_networks
    networks.sort(lambda a,b: cmp(a.quality.quality,
                                             b.quality.quality), 
                             None, True)

    return networks[0]

  @classmethod
  def topTen(clazz, interface):
    IOCapture.startCapture()
    networks = []

    try:
      w = Wireless(interface)
      networks = w.scan()
    finally:
      IOCapture.stopCapture()

    
    networks.sort(lambda a,b: cmp(a.quality.quality, b.quality.quality), 
                  None, True)

    print "Networks sorted by probable proximity"

    for network in enumerate(networks):
      print '    %s) %s (%s, %s)' % (network[0], network[1].essid,
                                     network[1].quality.siglevel,
                                     network[1].quality.quality)
      
    
