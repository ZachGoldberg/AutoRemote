from Trigger import Trigger
import triggers

class TimeChanged (Trigger):
   """
   A trigger which can fire when a certain amount of Time or a specific Time passes
   """
   def __init__(self, triggerdata):
      super(TimeChanged, self).__init__(triggerdata)

   def is_triggered(self, worlddata):
       if worlddata.now().wifi_location.bssid != worlddata.now(-1).wifi_location.bssid:
           if worlddata.now().wifi_location.bssid == self.trigger_bssid:
               return True
       return False

triggers.register_trigger(TimeChanged)
