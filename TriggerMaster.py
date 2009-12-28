
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
         if not self.check_valid_triggerdata(i):
            print "Invalid Trigger Found (%s)" % i
            continue
         
         loaded_triggers.append(classes_by_name[i['trigger_class']](i))

      return loaded_triggers

   def check_valid_triggerdata(self, triggerdict):
      return set([u"upnpaction", u"trigger_class"]).issubset(
         set(triggerdict.keys()))
         
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
  
  print "\n" * 3
      
  import simplejson

  master = TriggerMaster(simplejson.load(open('triggers.json')))
  print master
  
  import pdb
  pdb.set_trace()
