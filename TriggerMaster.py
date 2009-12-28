import triggers
from action import UPnPAction

class TriggerMaster(object):
   def __init__(self, triggerdata):
       self.triggerdata = triggerdata
       self.triggers = self.load_triggers(triggerdata)


   def load_triggers(self, triggerdata):
      classes = TriggerMaster.getTriggerTypes()
      classes_by_name = {}
      for i in classes:
         classes_by_name[i.__name__] = i
         
      loaded_triggers = []
      for i in triggerdata:         
         loaded_triggers.append(triggers.Trigger.Trigger.loads(i))

      return loaded_triggers

   @classmethod
   def getTriggerTypes(clz):
       return triggers.known_triggers

if __name__ == '__main__':

  import simplejson

  master = TriggerMaster(simplejson.load(open('triggers.json')))
  trig = triggers.Trigger.Trigger.loads(master.triggers[0].dumps())
  trigo = master.triggers[0]
  assert set(trig.__dict__.keys()) - set(trigo.__dict__.keys()) == set()
