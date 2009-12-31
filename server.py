from gi.repository import GLib, GUPnP, GUPnPAV, GSSDP, GObject, libsoup
import pdb
import pygtk, gtk, simplejson

from datetime import datetime
from action import UPnPAction
from UPnPDeviceManager import UPnPDeviceManager
from TriggerMaster import TriggerMaster
from WorldData import WorldData, WorldState

class AutoRemoteServer(object):
  def __init__(self, triggers):
    self.wifi_location = None
    self.triggers = triggers

  def main(self):

    self.device_mgr = UPnPDeviceManager()
    self.device_mgr.connect("device-available", self.device_available)
    self.device_mgr.connect("device-unavailable", self.device_unavailable)

    self.world = WorldData()
    self.triggermaster = TriggerMaster(simplejson.load(open('triggers.json')), self.device_mgr)
    
    GObject.timeout_add(5000, self.process_triggers)
    GObject.timeout_add(5000, self.device_mgr.list_cur_devices)

    import gtk
    gtk.main()

  def process_triggers(self):
    self.world.advance_time()
    self.triggermaster.run_triggers(self.world)
    return True
    

  def device_available(self, manager, device):
    print "Device available", device.get_friendly_name()
    
  def device_unavailable(self, manager, device):
    print "Device unavailable", device.get_friendly_name()

    
if __name__ == "__main__":
  prog = AutoRemoteServer(simplejson.load(open("./triggers.json")))
  prog.main()

