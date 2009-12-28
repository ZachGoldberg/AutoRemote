
import triggers
from action import UPnPAction

class TriggerMaster(object):
   def __init__(self, triggerdata):
       self.triggerdata = triggerdata
  
   @classmethod
   def getTriggerTypes(clz):
       return triggers.known_triggers

if __name__ == '__main__':
  action = UPnPAction("device", "service", "action", "{}")
  actions = action.dumps()

  for i in TriggerMaster.getTriggerTypes():
      print i.__name__, i.__doc__
      t = i({"upnpaction": actions, "trigger_bssid": "asdasd"})  
      print t
      print t.action
      print t.__dict__
