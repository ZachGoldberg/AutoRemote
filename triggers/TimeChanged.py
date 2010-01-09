from datetime import datetime, timedelta

from Trigger import Trigger
import triggers

class TimeChanged (Trigger):
   """
   A trigger which can fire when a certain amount of Time or a specific Time passes
   """
   def __init__(self, triggerdata):
      super(TimeChanged, self).__init__(triggerdata)      
      self.name = "Time based Trigger"

      self.checkpoint_time = datetime.now()
      if not hasattr(self, "time_delta"):
         self.time_delta = -1
         
      if not hasattr(self, "cycle_trigger"):
         self.cycle_trigger = False

   def is_triggered(self, worlddata):
      if not self.active:
         return False
      
      if self.time_delta > 0 and ((worlddata.now().get_time() - self.checkpoint_time) > timedelta(
         seconds=self.time_delta)):
         if self.cycle_trigger:
            self.checkpoint_time = datetime.now()
         return True
       
      return False

triggers.register_trigger(TimeChanged)
