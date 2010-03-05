from gi.repository import GLib, GUPnP, GUPnPAV, GSSDP, GObject, libsoup
import pdb
import pygtk, gtk, simplejson, sys, subprocess

from datetime import datetime
from util.action import UPnPAction
from controllers.UPnPDeviceManager import UPnPDeviceManager
from controllers.TriggerMaster import TriggerMaster
from controllers.WorldData import WorldData, WorldState

class AutoRemote(object):
  def __init__(self, triggers):
    self.wifi_location = None
    self.triggers = triggers

  def main(self):

    self.device_mgr = UPnPDeviceManager()
    self.device_mgr.connect("device-available", self.device_available)
    self.device_mgr.connect("device-unavailable", self.device_unavailable)

    try:
      from util.hildongui import HildonAutoRemoteGUI as AutoRemoteGUI
    except:
      import traceback
      traceback.print_exc()

    if not "AutoRemoteGUI" in dir():
      try:
        from util.gtkgui import GTKAutoRemoteGUI as AutoRemoteGUI
      except:
        import traceback
        traceback.print_exc()
        sys.stderr.write("Could not load either hildon or gtk frameworks.  Bailing out.\n")
        sys.exit(1)
      
    self.ui = AutoRemoteGUI(self.device_mgr)
    self.ui.remote = self
    
    self.load_data("triggers.json")

    GObject.timeout_add(1000, self.update_backend_status)

    self.ui.main()

  def update_backend_status(self):
    backend_name = "autoremote_backend.py"
    ps_data = subprocess.Popen(["ps", "-eo","pid,args"],
                               stdout=subprocess.PIPE).communicate()[0].split("\n")

    backend_status = False
    for i in ps_data:
      if backend_name in i:
        backend_status = True
        break

    self.ui.update_backend_status(backend_status)
       
    return True

  def add_trigger(self, trigger):
    data_file = "triggers.json"
    try:
      triggerdata = simplejson.load(open(data_file))
    except:
      triggerdata = []
      
    triggerdata.append(trigger.dumps())
    f = open(data_file, "w")
    f.write(simplejson.dumps(triggerdata))
    f.close()

  def write_triggers(self, triggers):
    data_file = "triggers.json"
    triggerdata = []
    for trigger in triggers:
      triggerdata.append(trigger.dumps())

    f = open(data_file, "w")
    f.write(simplejson.dumps(triggerdata))
    f.close()           

  def load_data(self, data_file):
    try:
      triggerdata = simplejson.load(open(data_file))
    except:
      triggerdata = []
      
    self.triggermaster = TriggerMaster(triggerdata, self.device_mgr)

    for trigger in self.triggermaster.triggers:
      self.ui.add_trigger(trigger)
      print trigger

  def device_available(self, manager, device):
    print "Device available", device.get_friendly_name(), device.get_udn()
    if device.is_renderer:
      self.ui.add_renderer(device)
    
  def device_unavailable(self, manager, device):
    print "Device unavailable", device.get_friendly_name()
    if device.is_renderer:
      self.ui.remove_renderer(device)

  def stop_object(self, source, renderer, item):
    av_serv = self.get_av_for_renderer(renderer)
    data = {"InstanceID": 0}
    av_serv.send_action_hash("Stop", data, {})

  def pause_object(self, source, renderer, item):
    av_serv = self.get_av_for_renderer(renderer)
    data = {"InstanceID": 0}
    av_serv.send_action_hash("Pause", data, {})
    
  def get_av_for_renderer(self, renderer):
    services = self.device_manager.device_services[renderer.get_udn()]
    av_serv = None
    for s in services:
      if "AVTransport" in s.get_service_type():
        av_serv = s
        break
    return av_serv
    
  def play_object(self, source, renderer, item):
    resources = item.get_resources()

    if not resources or len(resources) < 1:
	print "Could not get a resource for item to play!"
        import pdb
        pdb.set_trace()
	return

    uri = resources[0].get_uri()
    data = {"InstanceID": "0", "CurrentURI": uri, "CurrentURIMetaData": uri} 
    av_serv = self.get_av_for_renderer(renderer) 
    
    act = UPnPAction(renderer,
                     av_serv,
                     "SetAVTransportURI",
                     data)

    self.execute_action(act)
    data = {"InstanceID": "0", "CurrentURI": uri, "CurrentURIMetaData": uri, "Speed": 1} 
    act = UPnPAction(renderer,
                     av_serv,
                     "Play",
                     data)

    self.execute_action(act)


  def execute_action(self, action):
    if not action.is_executable():
      device = action.device_udn
      services = self.device_services[device]
      for s in services:
        if s.get_udn() == action.service_udn:
          action.service = s

    action.execute()

  def children_loaded(self, service, action, data):
    """
    Ends the action and loads the data
    """

    out_data = {"Result": "", "NumberReturned": "", "TotalMatches": "", "UpdateID": ""}

    success, return_data = service.end_action_hash(action, out_data)
    if not success:
      print "Browse Node Action Failed"

    parser = DIDLParser(return_data["Result"])

    self.ui.clear_source_browser()
    for c in parser.containers:
      self.ui.add_container(c)

    for o in parser.objects:
      self.ui.add_object(o)

  def load_children(self, device, object_id=0):
    """
    Make an asynchronous call to download the children of this node
    The UI will call this and then continue.  The calback for the
    async browse function will populate the UI
    """
    serv = self.device_manager.is_source(device.get_udn())
  
    assert serv

    in_data = {"ObjectID": object_id, "BrowseFlag": "BrowseDirectChildren",
               "Filter": "*", "StartingIndex": "0", "RequestCount": "0",
               "SortCriteria": ""}

    return_data = serv.begin_action_hash("Browse", self.children_loaded, None, in_data)
    if not return_data:
      print "Error initiating the Browse action"
  

if __name__ == "__main__":
  try:
    data = simplejson.load(open("./triggers.json"))
  except:
    data = []
    
  prog = AutoRemote(data)
  prog.main()

