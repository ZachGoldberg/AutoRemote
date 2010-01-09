from Trigger import Trigger
import triggers

class LocationChanged (Trigger):
   """
   A trigger which can fire when your WiFi Location changes to a certain new bssid
   """
   def __init__(self, triggerdata):
      super(LocationChanged, self).__init__(triggerdata)
      self.name = "Location Based Trigger"

   def is_triggered(self, worlddata):
       if worlddata.now().wifi_location.bssid != worlddata.now(-1).wifi_location.bssid:
           if worlddata.now().wifi_location.bssid == self.trigger_bssid:
               return True
       return False

triggers.register_trigger(LocationChanged)
