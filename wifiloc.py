from pythonwifi.iwlibs import Wireless
from iocapture import IOCapture



def getAvailableAPs():
  # pythonwifi has print statements... capture it and silence!
  IOCapture.startCapture()

  try:
      w = Wireless("eth1") 
      networks = w.scan()
  finally:
      IOCapture.stopCapture()

  return networks

def getCurrentAP():

  networks = getAvailableAPs()
  networks.sort(lambda a,b: cmp(a.quality.quality, b.quality.quality), None, True)

  return networks[0]

def topTen():
  networks = getAvailableAPs()

  networks.sort(lambda a,b: cmp(a.quality.quality, b.quality.quality), None, True)

  print "Networks sorted by probable proximity"

  for network in enumerate(networks):
      print '    %s) %s (%s, %s)'%(network[0],network[1].essid, network[1].quality.siglevel,network[1].quality.quality)

