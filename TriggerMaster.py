
import triggers

class TriggerMaster(object):
   def __init__(self, triggerdata):
       self.triggerdata = triggerdata
  
   @classmethod
   def getTriggerTypes(clz):
       return triggers.known_triggers

if __name__ == '__main__':
  for i in TriggerMaster.getTriggerTypes():
      print i.__name__, i.__doc__
    
