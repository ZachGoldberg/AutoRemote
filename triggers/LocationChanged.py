from Trigger import Trigger
from util import inputs
import triggers

class LocationChanged (Trigger):
   """
   A trigger which can fire when your WiFi Location changes to a certain new bssid
   """
   def __init__(self, triggerdata):
      super(LocationChanged, self).__init__(triggerdata)
      if not hasattr(self, "name") or not self.name:
         self.name = "Location Based Trigger"
         self.displayName = self.name
      else:
         self.displayName = self.name + " (WiFi Locatio)"


   def is_triggered(self, worlddata):
       if worlddata.now().wifi_location.bssid != worlddata.now(-1).wifi_location.bssid:
           if worlddata.now().wifi_location.bssid == self.trigger_bssid:
               return True
       return False

   @classmethod
   def get_editable_fields(clz):      
      return [inputs.Entry("Trigger when changing to (BSSID):",
                           userdata="trigger_bssid"),
              ]

triggers.register_trigger(LocationChanged)
