from gi.repository import GLib, GUPnP, GUPnPAV, GSSDP, GObject, libsoup
import os, urllib2, tempfile, atexit
import pdb
import pygtk, gtk

from gui import PyGUPnPCPUI
from action import UPnPAction
from UPnPDeviceManager import UPnPDeviceManager

class PyGUPnPCP(object):
  def __init__(self):
    self.devices = []
    self.introspections = {}
    self.device_services = {}
    
    self.sources = []
    self.renderers = []
    self.ui = None
    self.cps = []
    self.contexts = []  
    self.created_files = []

    atexit.register(self.cleanup_files)

  def cleanup_files(self):
    for i in self.created_files:
      os.unlink(i)
    

  def main(self):

    self.device_mgr = UPnPDeviceManager()
    self.device_mgr.connect("device-available", self.device_available)
    self.device_mgr.connect("device-unavailable", self.device_available)
    #self.ui = PyGUPnPCPUI(self)
    #self.ui.main()
    import gtk
    gtk.main()

  def device_available(self, manager, device):
    pass
  def device_unavailable(self, manager, device):
    pass


  def stop_object(self, source, renderer, item):
    av_serv = self.get_av_for_renderer(renderer)
    data = {"InstanceID": 0}
    av_serv.send_action_hash("Stop", data, {})

  def pause_object(self, source, renderer, item):
    av_serv = self.get_av_for_renderer(renderer)
    data = {"InstanceID": 0}
    av_serv.send_action_hash("Pause", data, {})
    
  def get_av_for_renderer(self, renderer):
    services = self.device_services[renderer.get_udn()]
    av_serv = None
    for s in services:
      if "AVTransport" in s.get_service_type():
        av_serv = s
        break
    return av_serv
    
  def play_object(self, source, renderer, item):
    resources = item.get_resources()
    if len(resources) < 1:
	print "Could not get a resource for item to play!"
	return

    uri = resources[0].get_uri()
    data = {"InstanceID": "0", "CurrentURI": uri, "CurrentURIMetaData": uri} 
    av_serv = self.get_av_for_renderer(renderer) 
    
    act = UPnPAction(renderer,
                     av_serv,
                     "SetAVTransportURI",
                     data)

    self.execute_action(act)
    
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
    serv = self.is_source(device.get_udn())
  
    assert serv

    in_data = {"ObjectID": object_id, "BrowseFlag": "BrowseDirectChildren",
               "Filter": "", "StartingIndex": "0", "RequestCount": "0",
               "SortCriteria": ""}

    return_data = serv.begin_action_hash("Browse", self.children_loaded, None, in_data)
    if not return_data:
      print "Error initiating the Browse action"
  


if __name__ == "__main__":
  prog = PyGUPnPCP()
  prog.main()







#  for service in device_services[device.get_udn()]:
#      introspections.remove(service.get_udn())

#  if device.get_model_name() == "MediaTomb":
#      for service in device.list_services():
#          print service.get_service_type()
#          if "ContentDirectory" in service.get_service_type():
#              service.get_introspection_async(server_introspection, None)



#  actions = intro.list_actions()
#  print len(actions)
#  for i in actions:
#      print service.get_service_type(), i.name      
#      if i.name == "SetAVTransportURI":
#          dict = {"Speed": "1", "InstanceID": "0"}
#          muri = "http://192.168.1.55:49152/content/media/object_id=6327&res_id=0&ext=.mp3"
#          curi = "http://192.168.1.55:49152/content/media/object_id=6327&res_id=0&ext=.mp3"
#          data = {"InstanceID": "0", "CurrentURI": curi, "CurrentURIMetaData": muri} 
#          service.send_action_hash(i.name, data, {})
#	  print "Done setting URI"
#          data2 = {"Speed": "1", "InstanceID": "0"}
#          service.send_action_hash("Stop", {"InstanceID": 0}, {})
#          print "Done Stopping"
#          service.send_action_hash("Play", data2, {})


  

#def server_introspection(service, introspection, error, userdata):
#  print "Got server introspection"
#  for i in introspection.list_actions():
#      if i.name == "Browse":
#         in_data = {"ObjectID": "0", "BrowseFlag": "BrowseDirectChildren",
#		    "Filter": "", "StartingIndex": "0", "RequestCount": "0",
#		    "SortCriteria": ""}
#         out_data = {"Result": "", "NumberReturned": "", "TotalMatches": "", "UpdateID": ""}#
#	 print "SEND ACTION"
#         return_data = service.send_action_hash("Browse", in_data, out_data)
#	 global serv
#	 serv=service
#	 print "Good news!"
#	 print return_data[1]["Result"]
#	 parser = GUPnPAV.GUPnPDIDLLiteParser()
#	 parser.connect("container_available", new_container)
#	 parser.connect("item_available", new_item)
#	 parser.parse_didl(return_data[1]["Result"])
#	 print len(objects)

