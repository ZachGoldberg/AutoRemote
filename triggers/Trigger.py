from action import UPnPAction
import simplejson, triggers

class Trigger(object):
   def __init__(self, triggerdata):
      for key, value in triggerdata.items():
          setattr(self, key, value)

      self.action = UPnPAction.loads(triggerdata["upnpaction"])
      
   def is_triggered(world_data):
      return False

   def dumps(self):
      data = self.__dict__.copy()
      if "action" in data:
         del data["action"]
      
      return simplejson.dumps(data)

   @classmethod
   def loads(clz, str):
      if isinstance(str, basestring):
         data = simplejson.loads(str)
      else:
         data = str

      if not Trigger.check_valid_triggerdata(data):
         raise Exception("Invalid Trigger Found (%s)" % data)
         
      clzname = data["trigger_class"]
      return triggers.triggers_by_name()[clzname](data)

   @classmethod
   def check_valid_triggerdata(clz, triggerdict):
      return set([u"upnpaction", u"trigger_class"]).issubset(
         set(triggerdict.keys()))
