import triggers
from util.action import UPnPAction

class TriggerMaster(object):
   def __init__(self, triggerdata, device_mgr):
       self.triggerdata = triggerdata
       self.device_mgr = device_mgr
       self.triggers = self.load_triggers(triggerdata)


   def load_triggers(self, triggerdata):
      classes = TriggerMaster.getTriggerTypes()
      classes_by_name = {}
      for i in classes:
         classes_by_name[i.__name__] = i
         
      loaded_triggers = []
      for i in triggerdata:
         trigger = triggers.Trigger.Trigger.loads(i)
         loaded_triggers.append(trigger)
         trigger.action.register_device_manager(self.device_mgr)
         
      return loaded_triggers

   def run_triggers(self, world):
      
      for trigger in self.triggers:            
         if trigger.is_triggered(world):            
            trigger.execute_action()
            if not trigger.reusable:
               trigger.active = False
   

   @classmethod
   def getTriggerTypes(clz):
       return triggers.known_triggers

if __name__ == '__main__':

  import simplejson

  master = TriggerMaster(simplejson.load(open('triggers.json')))
  trig = triggers.Trigger.Trigger.loads(master.triggers[0].dumps())
  trigo = master.triggers[0]
  assert set(trig.__dict__.keys()) - set(trigo.__dict__.keys()) == set()
