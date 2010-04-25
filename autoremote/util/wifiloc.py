from pythonwifi.iwlibs import Wireless, getNICnames
from iocapture import IOCapture

class WifiLoc(object):

  def __init__(self):
    try:
        self.interfaces = getNICnames()
    except:
        self.interfaces = []

    self.known_networks = {}
    self.wifis = []
    for i in self.interfaces:
      self.wifis.append(Wireless(i))

  def update_location(self):
    IOCapture.startCapture()
    networks = []

    try:
      for i in self.wifis:
        networks.extend(i.scan())
    except:
      IOCapture.stopCapture()
      print "Error during scanning, perhaps you don't have permission?"
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

    if networks:
      return networks[0]
    else:
      return None

  @classmethod
  def topTen(clazz):
    IOCapture.startCapture()
    networks = []

    try:
      for i in getNICnames():
        w = Wireless(i)
        networks.extend(w.scan())
    finally:
      IOCapture.stopCapture()

    
    networks.sort(lambda a,b: cmp(a.quality.quality, b.quality.quality), 
                  None, True)

    print "Networks sorted by probable proximity"

    for network in enumerate(networks):
      print '    %s) %s (%s, %s)' % (network[0], network[1].essid,
                                     network[1].quality.siglevel,
                                     network[1].quality.quality)
      
    
