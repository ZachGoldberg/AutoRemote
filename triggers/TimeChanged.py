from datetime import datetime, timedelta

from Trigger import Trigger
import triggers

from util import inputs

class TimeChanged (Trigger):
   """
   A trigger which can fire when a certain amount of Time or a specific Time passes
   """
   def __init__(self, triggerdata):
      super(TimeChanged, self).__init__(triggerdata)
      
      if not hasattr(self, "name") or not self.name:
         self.name = "Time Based Trigger"
         self.displayName = self.name
      else:
         self.displayName = self.name + " (Time)"

      self.checkpoint_time = datetime.now()
      if not hasattr(self, "time_delta"):
         self.time_delta = -1
      else:
         self.time_delta = int(self.time_delta)
         
      if not hasattr(self, "cycle_trigger"):
         self.cycle_trigger = True
   
   def is_triggered(self, worlddata):
      if not self.active:
         return False
      
      if self.time_delta > 0 and ((worlddata.now().get_time() - self.checkpoint_time) > timedelta(
         seconds=self.time_delta)):
         print self.cycle_trigger
         if self.cycle_trigger:
            self.checkpoint_time = datetime.now()
         return True
       
      return False

   def dumps(self):
      self.checkpoint_time = ""
      return super(TimeChanged, self).dumps()
   
   @classmethod
   def get_editable_fields(clz):
      return [inputs.Selection("Time Type", ["Specific Time",
                                             "Elapsed TIme"],
                               userdata="trigger_style"),
              inputs.Entry("Specific Time: (%HH/%MM format) \n"
                           "or interval time (in seconds) ",
                           userdata="time_delta")
              ]
   

triggers.register_trigger(TimeChanged)
